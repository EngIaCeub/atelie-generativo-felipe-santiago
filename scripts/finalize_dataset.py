from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError

ALLOWED_LICENSE_PREFIXES = ("Public domain", "CC0", "CC-BY ", "CC-BY-SA ", "Autoria propria")
REQUIRED_SOURCE_FIELDS = {
    "arquivo",
    "arquivo_final",
    "url",
    "autor",
    "licenca",
    "origem_tipo",
    "transformacao_ia",
    "ferramenta_modelo",
    "observacoes",
}
ADMIN_PATTERN = re.compile(r"https?://|www\.|\bimg_\d+\.(?:png|jpe?g|webp)\b|\b(?:cc0|cc-by|wikimedia|licen[cs]a)\b", re.I)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


@dataclass
class ItemAudit:
    arquivo: str
    arquivo_final: str
    approved: bool
    reasons: list[str]
    caption: str | None = None


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_captions(path: Path) -> dict[str, tuple[str, str]]:
    captions: dict[str, tuple[str, str]] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            raise ValueError(f"Linha de caption malformada: {line!r}")
        filename, caption, status = (part.strip() for part in parts)
        if filename in captions:
            raise ValueError(f"Caption duplicada para {filename}")
        captions[filename] = (caption, status)
    return captions


def source_image_path(root: Path, source: dict[str, str]) -> Path:
    candidate = Path(source["arquivo_final"])
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"Caminho final inseguro: {candidate}")
    return root / candidate


def caption_is_valid(caption: str, token: str) -> bool:
    return caption.startswith(f"{token},") and not ADMIN_PATTERN.search(caption)


def is_allowed_license(value: str) -> bool:
    return value.strip().startswith(ALLOWED_LICENSE_PREFIXES)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_dataset(root: Path) -> tuple[list[ItemAudit], dict[str, object]]:
    config = json.loads((root / "config/project.json").read_text(encoding="utf-8"))
    token = str(config["style"]["trigger_token"])
    sources = read_csv(root / "dados/fontes.csv")
    captions = read_captions(root / "dados/legendas.txt")
    triage = {row["arquivo"]: row for row in read_csv(root / "resultados/auditorias/dataset_triagem_2026-07-10.csv")}
    manifest = json.loads((root / "resultados/auditorias/dataset_manifest_2026-07-10.json").read_text(encoding="utf-8"))
    manifest_items = {item["arquivo"]: item for item in manifest["items"]}
    output_files = {
        path.name
        for path in (root / "dados/imagens").glob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    }
    source_files = {row.get("arquivo", "").strip() for row in sources}
    audits: list[ItemAudit] = []

    for source in sources:
        filename = source.get("arquivo", "").strip()
        reasons: list[str] = []
        if not filename or any(not source.get(field, "").strip() for field in REQUIRED_SOURCE_FIELDS):
            reasons.append("proveniencia incompleta")
        try:
            image_path = source_image_path(root, source)
        except (KeyError, ValueError) as exc:
            image_path = root / "dados/imagens" / filename
            reasons.append(str(exc))
        if not image_path.is_file():
            reasons.append("imagem final ausente")
        else:
            try:
                with Image.open(image_path) as image:
                    if min(image.size) < 512:
                        reasons.append("resolucao final abaixo de 512 px")
            except (OSError, UnidentifiedImageError):
                reasons.append("imagem final ilegivel")
        if not is_allowed_license(source.get("licenca", "")):
            reasons.append("licenca nao permitida")
        if source.get("transformacao_ia", "").strip().casefold().startswith("sim") and not source.get("origem_tipo", "").startswith(("derivada", "sintetica")):
            reasons.append("transformacao por IA sem classificacao derivada ou sintetica")
        if source.get("origem_tipo", "").startswith("derivada") and source.get("transformacao_ia", "").strip().casefold().startswith("sim"):
            reasons.append("transformacao por IA declarada; requer trilha especifica de modelo e prompt")
        triage_row = triage.get(filename, {})
        if triage_row.get("coerencia_visual") != "sim" or triage_row.get("decisao") != "aceita":
            reasons.append("triagem visual nao aceita")
        for field in ("marca_dagua", "assinatura_problematica", "ip_protegida", "pessoa_identificavel"):
            if triage_row.get(field) != "nao":
                reasons.append(f"triagem sinaliza {field}")
        manifest_item = manifest_items.get(filename)
        if not manifest_item:
            reasons.append("item ausente do manifesto")
        elif image_path.is_file() and manifest_item.get("output_sha256") != file_sha256(image_path):
            reasons.append("hash do arquivo final diverge do manifesto")
        caption, status = captions.get(filename, ("", ""))
        if status != "revisada":
            reasons.append("caption nao marcada como revisada")
        if not caption_is_valid(caption, token):
            reasons.append("caption sem token valido ou com metadado administrativo")
        audits.append(ItemAudit(filename, str(source.get("arquivo_final", "")), not reasons, reasons, caption or None))

    if source_files != output_files:
        missing_sources = sorted(output_files - source_files)
        orphan_sources = sorted(source_files - output_files)
        for item in audits:
            if missing_sources or orphan_sources:
                item.approved = False
                item.reasons.append(f"correspondencia fonte/imagem invalida: sem fonte={missing_sources}; sem imagem={orphan_sources}")
    if manifest.get("near_duplicate_pairs"):
        for item in audits:
            item.approved = False
            item.reasons.append("manifesto registra duplicatas perceptuais")
    summary = {
        "style": config["style"]["name"],
        "trigger_token": token,
        "source_count": len(sources),
        "approved_count": sum(item.approved for item in audits),
        "rejected_or_pending_count": sum(not item.approved for item in audits),
        "near_duplicate_pairs": manifest.get("near_duplicate_pairs", []),
        "caption_method": "inspecao visual e metadados; revisao humana",
        "blip": "nao executado localmente: torch e transformers indisponiveis",
    }
    return audits, summary


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_metadata(path: Path, audits: list[ItemAudit]) -> None:
    approved = [item for item in audits if item.approved and item.caption]
    temporary = path.with_suffix(".jsonl.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        for item in approved:
            handle.write(json.dumps({"file_name": item.arquivo_final, "text": item.caption}, ensure_ascii=False) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita o dataset final e exporta metadata somente quando aprovado.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--write-metadata", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    audits, summary = audit_dataset(root)
    payload = {"summary": summary, "items": [asdict(item) for item in audits]}
    report_path = args.report if args.report.is_absolute() else root / args.report
    write_json(report_path, payload)
    if summary["rejected_or_pending_count"]:
        print(f"Auditoria reprovada: {summary['approved_count']}/{summary['source_count']} itens aprovados.")
        return 1
    if args.write_metadata:
        write_metadata(root / "dados/metadata.jsonl", audits)
        print(f"Auditoria aprovada; metadata gerado com {summary['approved_count']} registros.")
    else:
        print(f"Auditoria aprovada; {summary['approved_count']} itens elegiveis. Metadata nao solicitado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
