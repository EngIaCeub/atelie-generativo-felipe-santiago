from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import re
import shutil
import time
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFilter, ImageOps, PngImagePlugin, UnidentifiedImageError

USER_AGENT = "AtelieGenerativoDatasetCurator/1.0 (academic project)"
PROCESSING_VERSION = "woodcut-v2"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SOURCE_FIELDS = ["arquivo", "url", "autor", "licenca", "data_coleta", "fonte", "observacoes"]
UNKNOWN_AUTHOR_MARKERS = ("unknown", "anonymous", "no machine-readable", "desconhecid")


class CurationError(RuntimeError):
    pass


def request_bytes(url: str, *, attempts: int = 5) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=60) as response:  # noqa: S310 - curated HTTPS URLs only
                return response.read()
        except HTTPError as exc:
            if attempt == attempts - 1:
                raise CurationError(f"Falha ao acessar {url}: {exc}") from exc
            retry_after = exc.headers.get("Retry-After") if exc.code == 429 else None
            time.sleep(float(retry_after) if retry_after else 5 * (attempt + 1))
        except (URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise CurationError(f"Falha ao acessar {url}: {exc}") from exc
            time.sleep(2 ** (attempt + 1))
    raise AssertionError("retry loop exhausted")


def request_json(api_url: str, params: dict[str, str]) -> dict[str, Any]:
    url = f"{api_url}?{urlencode(params)}"
    try:
        return json.loads(request_bytes(url).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CurationError(f"Resposta inválida da API: {url}") from exc


def clean_html(value: object) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<br\s*/?>", "; ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split())


def ext_value(metadata: dict[str, Any], key: str) -> str:
    item = metadata.get(key, {})
    return clean_html(item.get("value", "") if isinstance(item, dict) else "")


def canonical_license(value: str) -> str:
    if value in {"CC0", "Public domain"}:
        return value
    match = re.fullmatch(r"CC BY(-SA)? (\d\.\d)", value)
    if match:
        suffix = "-SA" if match.group(1) else ""
        return f"CC-BY{suffix} {match.group(2)}"
    raise CurationError(f"Licença não permitida ou ambígua: {value or '<vazia>'}")


def query_source_pages(api_url: str, titles: list[str]) -> dict[str, dict[str, Any]]:
    pages_by_title: dict[str, dict[str, Any]] = {}
    normalized: dict[str, str] = {}
    for start in range(0, len(titles), 8):
        batch = titles[start : start + 8]
        payload = request_json(
            api_url,
            {
                "action": "query",
                "format": "json",
                "formatversion": "2",
                "prop": "imageinfo|info",
                "inprop": "url",
                "iiprop": "url|size|mime|extmetadata|sha1",
                "iiurlwidth": "1024",
                "titles": "|".join(batch),
            },
        )
        query = payload.get("query", {})
        normalized.update(
            {item["from"]: item["to"] for item in query.get("normalized", [])}
        )
        pages_by_title.update(
            {page.get("title", ""): page for page in query.get("pages", [])}
        )

    result: dict[str, dict[str, Any]] = {}
    for title in titles:
        page = pages_by_title.get(normalized.get(title, title))
        if not page or page.get("missing"):
            raise CurationError(f"Arquivo não encontrado no Wikimedia Commons: {title}")
        result[title] = page
    return result


def validate_source(page: dict[str, Any]) -> dict[str, Any]:
    image_info = (page.get("imageinfo") or [None])[0]
    if not isinstance(image_info, dict):
        raise CurationError(f"Metadados de imagem ausentes: {page.get('title')}")

    width = int(image_info.get("width", 0))
    height = int(image_info.get("height", 0))
    if min(width, height) < 512:
        raise CurationError(
            f"Original abaixo de 512 x 512: {page.get('title')} ({width} x {height})"
        )
    if image_info.get("mime") not in {"image/jpeg", "image/png", "image/webp"}:
        raise CurationError(f"Formato não permitido: {page.get('title')}")

    metadata = image_info.get("extmetadata") or {}
    author = ext_value(metadata, "Artist")
    if not author or any(marker in author.casefold() for marker in UNKNOWN_AUTHOR_MARKERS):
        raise CurationError(f"Autoria não verificável: {page.get('title')} ({author})")

    source_license = ext_value(metadata, "LicenseShortName")
    license_code = canonical_license(source_license)
    page_url = str(page.get("canonicalurl", ""))
    download_url = str(image_info.get("url", ""))
    processing_url = str(image_info.get("thumburl") or download_url)
    if not page_url.startswith("https://commons.wikimedia.org/"):
        raise CurationError(f"URL de página inesperada: {page_url}")
    if not download_url.startswith("https://upload.wikimedia.org/"):
        raise CurationError(f"URL de arquivo inesperada: {download_url}")
    if not processing_url.startswith("https://upload.wikimedia.org/"):
        raise CurationError(f"URL de processamento inesperada: {processing_url}")

    processing_width = int(image_info.get("thumbwidth") or width)
    processing_height = int(image_info.get("thumbheight") or height)
    if min(processing_width, processing_height) < 512:
        raise CurationError(
            f"Fonte de processamento abaixo de 512 x 512: {page.get('title')} "
            f"({processing_width} x {processing_height})"
        )

    return {
        "source_title": page.get("title", ""),
        "source_page_url": page_url,
        "source_download_url": download_url,
        "processing_download_url": processing_url,
        "source_author": author,
        "source_license": license_code,
        "source_license_label": source_license,
        "source_license_url": ext_value(metadata, "LicenseUrl") or None,
        "source_description": ext_value(metadata, "ImageDescription") or None,
        "source_credit": ext_value(metadata, "Credit") or None,
        "source_dimensions": [width, height],
        "processing_source_dimensions_reported": [processing_width, processing_height],
        "source_mime": image_info.get("mime"),
        "source_mediawiki_sha1": image_info.get("sha1"),
        "source_page_revision": page.get("lastrevid"),
    }


def hatch_pattern(size: int, *, spacing: int, descending: bool) -> Image.Image:
    pattern = Image.new("RGB", (size, size), (246, 240, 222))
    draw = ImageDraw.Draw(pattern)
    for offset in range(-size, size * 2, spacing):
        if descending:
            draw.line((offset, 0, offset - size, size), fill=(18, 18, 16), width=1)
        else:
            draw.line((offset, 0, offset + size, size), fill=(18, 18, 16), width=1)
    return pattern


def render_woodcut(image: Image.Image, size: int, centering: tuple[float, float]) -> Image.Image:
    fitted = ImageOps.fit(
        ImageOps.exif_transpose(image).convert("RGB"),
        (size, size),
        method=Image.Resampling.LANCZOS,
        centering=centering,
    )
    grayscale = ImageOps.autocontrast(
        ImageOps.grayscale(fitted).filter(ImageFilter.MedianFilter(3)), cutoff=1
    )
    result = Image.new("RGB", (size, size), (246, 240, 222))

    dark_mask = grayscale.point(lambda pixel: 255 if pixel < 52 else 0)
    result.paste((18, 18, 16), mask=dark_mask)

    mid_mask = grayscale.point(lambda pixel: 255 if 52 <= pixel < 158 else 0)
    result = Image.composite(
        hatch_pattern(size, spacing=11, descending=True), result, mid_mask
    )

    cross_mask = grayscale.point(lambda pixel: 255 if 52 <= pixel < 96 else 0)
    result = Image.composite(
        hatch_pattern(size, spacing=17, descending=False), result, cross_mask
    )

    edge_strength = ImageOps.autocontrast(grayscale.filter(ImageFilter.FIND_EDGES), cutoff=2)
    edge_mask = edge_strength.point(lambda pixel: 255 if pixel > 92 else 0)
    result.paste((18, 18, 16), mask=edge_mask)
    return result


def png_metadata(source: dict[str, Any], collected_on: str) -> PngImagePlugin.PngInfo:
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("SourceTitle", str(source["source_title"]))
    metadata.add_text("Source", str(source["source_page_url"]))
    metadata.add_text("Author", str(source["source_author"]))
    metadata.add_text("License", str(source["source_license"]))
    metadata.add_text("CollectedOn", collected_on)
    metadata.add_text("ProcessingVersion", PROCESSING_VERSION)
    metadata.add_text(
        "ProcessingSourceSHA256", str(source.get("processing_source_sha256") or "")
    )
    processing_dimensions = source.get("processing_source_dimensions")
    metadata.add_text(
        "ProcessingSourceDimensions",
        "x".join(str(value) for value in processing_dimensions)
        if processing_dimensions
        else "",
    )
    metadata.add_text(
        "Transformation",
        "Deterministic square crop, monochrome contrast, edge emphasis and hatching; "
        "distributed under the source license.",
    )
    return metadata


def cached_output_metadata(
    path: Path, source: dict[str, Any], collected_on: str, size: int
) -> dict[str, Any]:
    try:
        with Image.open(path) as cached:
            cached.load()
            if cached.size != (size, size):
                raise CurationError(f"Cache com dimensão inválida: {path}")
            expected = {
                "SourceTitle": source["source_title"],
                "Source": source["source_page_url"],
                "Author": source["source_author"],
                "License": source["source_license"],
                "CollectedOn": collected_on,
                "ProcessingVersion": PROCESSING_VERSION,
            }
            for key, value in expected.items():
                if cached.info.get(key) != value:
                    raise CurationError(f"Cache incompatível em {path}: campo {key}")
            processing_sha256 = cached.info.get("ProcessingSourceSHA256") or None
            dimensions_text = cached.info.get("ProcessingSourceDimensions") or ""
    except (UnidentifiedImageError, OSError) as exc:
        raise CurationError(f"Cache de imagem inválido: {path}") from exc

    processing_dimensions: list[int] | None = None
    if dimensions_text:
        try:
            processing_dimensions = [int(value) for value in dimensions_text.split("x")]
        except ValueError as exc:
            raise CurationError(f"Dimensões inválidas no cache: {path}") from exc
    return {
        "processing_source_sha256": processing_sha256,
        "processing_source_dimensions": processing_dimensions,
        "output_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "output_dhash": image_dhash(path),
        "cache_recovered": processing_sha256 is None,
    }


def image_dhash(path: Path) -> str:
    with Image.open(path) as image:
        grayscale = image.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
        pixels = grayscale.load()
        value = 0
        for y in range(8):
            for x in range(8):
                value = (value << 1) | int(pixels[x, y] > pixels[x + 1, y])
    return f"{value:016x}"


def hash_distance(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def near_duplicate_pairs(items: list[dict[str, Any]], threshold: int = 8) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for index, left in enumerate(items):
        for right in items[index + 1 :]:
            distance = hash_distance(str(left["output_dhash"]), str(right["output_dhash"]))
            if distance <= threshold:
                pairs.append(
                    {
                        "arquivo_a": left["arquivo"],
                        "arquivo_b": right["arquivo"],
                        "dhash_hamming_distance": distance,
                    }
                )
    return pairs


def write_sources_csv(path: Path, rows: list[dict[str, str]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOURCE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def write_contact_sheet(path: Path, images_dir: Path, filenames: list[str]) -> None:
    columns = 4
    tile_size = 256
    label_height = 28
    rows = (len(filenames) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (columns * tile_size, rows * (tile_size + label_height)),
        (255, 255, 255),
    )
    draw = ImageDraw.Draw(sheet)
    for index, filename in enumerate(filenames):
        with Image.open(images_dir / filename) as image:
            tile = ImageOps.fit(
                image.convert("RGB"),
                (tile_size, tile_size),
                method=Image.Resampling.LANCZOS,
            )
        x = (index % columns) * tile_size
        y = (index // columns) * (tile_size + label_height)
        sheet.paste(tile, (x, y))
        draw.text((x + 8, y + tile_size + 7), filename, fill=(18, 18, 16))
    temporary = path.with_suffix(path.suffix + ".tmp")
    sheet.save(temporary, format="PNG", optimize=True)
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coleta e prepara o dataset aprovado usando metadados do Wikimedia Commons."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--date", required=True, help="Data de coleta em ISO 8601 (AAAA-MM-DD).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        date.fromisoformat(args.date)
    except ValueError as exc:
        raise CurationError("--date deve usar o formato AAAA-MM-DD") from exc

    root = args.root.resolve()
    selection_path = root / "config/dataset_sources.json"
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    items = selection.get("items", [])
    if not 20 <= len(items) <= 40:
        raise CurationError(f"Seleção deve conter 20 a 40 itens; encontrados {len(items)}")

    filenames = [str(item.get("filename", "")) for item in items]
    titles = [str(item.get("title", "")) for item in items]
    if len(filenames) != len(set(filenames)) or len(titles) != len(set(titles)):
        raise CurationError("Nomes de arquivo e títulos de fonte devem ser únicos")
    if any(Path(name).suffix.lower() != ".png" for name in filenames):
        raise CurationError("Todas as saídas selecionadas devem usar a extensão .png")

    images_dir = root / "dados/imagens"
    images_dir.mkdir(parents=True, exist_ok=True)
    unexpected = sorted(
        path.name
        for path in images_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
        and path.name not in set(filenames)
    )
    if unexpected:
        raise CurationError(f"Imagens fora da seleção: {', '.join(unexpected)}")

    pages = query_source_pages(str(selection["api_url"]), titles)
    size = int(selection.get("output_size", 768))
    if size < 512:
        raise CurationError("output_size deve ser pelo menos 512")

    source_rows: list[dict[str, str]] = []
    manifest_items: list[dict[str, Any]] = []
    cache_dir = images_dir / ".curation-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    legacy_cache_dirs = sorted(
        (path for path in images_dir.glob("dataset-*") if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for item in items:
        filename = str(item["filename"])
        title = str(item["title"])
        centering_values = item.get("centering", [0.5, 0.5])
        centering = (float(centering_values[0]), float(centering_values[1]))
        if not all(0.0 <= value <= 1.0 for value in centering):
            raise CurationError(f"Centering inválido para {filename}: {centering}")

        source = validate_source(pages[title])
        cache_path = cache_dir / filename
        if not cache_path.exists():
            candidates = [images_dir / filename]
            candidates.extend(directory / filename for directory in legacy_cache_dirs)
            recovered = next((path for path in candidates if path.exists()), None)
            if recovered:
                shutil.copy2(recovered, cache_path)

        cache_metadata: dict[str, Any] | None = None
        if cache_path.exists():
            try:
                cache_metadata = cached_output_metadata(cache_path, source, args.date, size)
            except CurationError as exc:
                print(f"Cache invalidado para {filename}: {exc}")
                cache_path.unlink()

        if cache_path.exists() and cache_metadata is not None:
            source["processing_source_sha256"] = cache_metadata[
                "processing_source_sha256"
            ]
            source["processing_source_dimensions"] = cache_metadata[
                "processing_source_dimensions"
            ]
            output_sha256 = cache_metadata["output_sha256"]
            output_dhash = cache_metadata["output_dhash"]
            cache_recovered = bool(cache_metadata["cache_recovered"])
        else:
            processing_bytes = request_bytes(source["processing_download_url"])
            source["processing_source_sha256"] = hashlib.sha256(processing_bytes).hexdigest()
            try:
                with Image.open(io.BytesIO(processing_bytes)) as opened:
                    opened.load()
                    actual_dimensions = list(opened.size)
                    if min(actual_dimensions) < 512:
                        raise CurationError(
                            f"Fonte baixada abaixo de 512 x 512 para {title}: {actual_dimensions}"
                        )
                    reported = source["processing_source_dimensions_reported"]
                    reported_ratio = reported[0] / reported[1]
                    actual_ratio = actual_dimensions[0] / actual_dimensions[1]
                    if abs(reported_ratio - actual_ratio) / reported_ratio > 0.02:
                        raise CurationError(
                            f"Proporção baixada diverge da API para {title}: "
                            f"informada={reported}, baixada={actual_dimensions}"
                        )
                    source["processing_source_dimensions"] = actual_dimensions
                    rendered = render_woodcut(opened, size, centering)
            except (UnidentifiedImageError, OSError) as exc:
                raise CurationError(f"Arquivo de imagem inválido: {title}") from exc

            rendered.save(
                cache_path,
                format="PNG",
                optimize=True,
                pnginfo=png_metadata(source, args.date),
            )
            output_sha256 = hashlib.sha256(cache_path.read_bytes()).hexdigest()
            output_dhash = image_dhash(cache_path)
            cache_recovered = False
            time.sleep(3)

        source_rows.append(
            {
                "arquivo": filename,
                "url": source["source_page_url"],
                "autor": source["source_author"],
                "licenca": source["source_license"],
                "data_coleta": args.date,
                "fonte": str(selection["source"]),
                "observacoes": (
                    "Derivação técnica local em preto e marfim, com recorte, contraste e "
                    "hachuras; distribuída sob a mesma licença da fonte; metadados verificados "
                    f"via API do Wikimedia Commons em {args.date}."
                ),
            }
        )
        manifest_items.append(
            {
                "arquivo": filename,
                **source,
                "centering": list(centering),
                "output_dimensions": [size, size],
                "output_sha256": output_sha256,
                "output_dhash": output_dhash,
                "processing_version": PROCESSING_VERSION,
                "cache_recovered_after_timeout": cache_recovered,
                "visual_review_status": "pending",
            }
        )

    for filename in filenames:
        shutil.copy2(cache_dir / filename, images_dir / filename)

    write_contact_sheet(
        root / "resultados/auditorias/dataset_contato_2026-07-10.png",
        images_dir,
        filenames,
    )

    write_sources_csv(root / "dados/fontes.csv", source_rows)
    write_json(
        root / "resultados/auditorias/dataset_manifest_2026-07-10.json",
        {
            "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "collection_date": args.date,
            "source": selection["source"],
            "api_url": selection["api_url"],
            "selection_file": str(selection_path.relative_to(root)).replace("\\", "/"),
            "processing": {
                "script": "scripts/collect_dataset.py",
                "version": PROCESSING_VERSION,
                "output_size": [size, size],
                "palette": ["#121210", "#F6F0DE"],
                "operations": [
                    "center_crop",
                    "grayscale",
                    "autocontrast",
                    "tone_threshold",
                    "diagonal_hatching",
                    "edge_emphasis",
                ],
            },
            "near_duplicate_pairs": near_duplicate_pairs(manifest_items),
            "items": manifest_items,
        },
    )
    print(f"Dataset preparado: {len(manifest_items)} imagens em {size} x {size}.")
    print("Proveniência: dados/fontes.csv")
    print("Manifesto: resultados/auditorias/dataset_manifest_2026-07-10.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
