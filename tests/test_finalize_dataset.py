from pathlib import Path

from scripts.finalize_dataset import caption_is_valid, is_allowed_license, read_captions


def test_caption_requires_token_and_rejects_administrative_text() -> None:
    assert caption_is_valid("flpxilobr, ave em galho com hachuras", "flpxilobr")
    assert not caption_is_valid("ave em galho com hachuras", "flpxilobr")
    assert not caption_is_valid("flpxilobr, ver https://example.test", "flpxilobr")
    assert not caption_is_valid("flpxilobr, arquivo img_001.png", "flpxilobr")


def test_dataset_license_allowlist() -> None:
    assert is_allowed_license("CC-BY-SA 4.0")
    assert is_allowed_license("CC-BY 4.0")
    assert is_allowed_license("CC0")
    assert not is_allowed_license("CC-BY-NC 4.0")


def test_caption_reader_accepts_utf8_bom(tmp_path: Path) -> None:
    path = tmp_path / "legendas.txt"
    path.write_text("# arquivo<TAB>caption<TAB>status_revisao\nimg_001.png\tflpxilobr, flor\trevisada\n", encoding="utf-8-sig")

    assert read_captions(path) == {"img_001.png": ("flpxilobr, flor", "revisada")}
