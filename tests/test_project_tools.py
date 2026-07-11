from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from scripts.check_secrets import scan
from scripts.project_status import (
    REQUIRED_TEAM_ASSIGNMENTS,
    bootstrap_checks,
    collect,
    dataset_checks,
)


def test_scaffold_has_no_secret_patterns() -> None:
    assert scan(Path.cwd()) == []


def test_project_config_is_valid_json() -> None:
    data = json.loads(Path("config/project.json").read_text(encoding="utf-8"))
    assert data["project_name"] == "atelie-generativo-felipe-santiago"
    assert data["hugging_face"]["token_status"] == "available_not_versioned"


def test_status_collects_all_stages() -> None:
    stages = collect(Path.cwd())
    assert set(stages) == {"bootstrap", "dataset", "training", "evaluation", "publication", "final"}


def base_bootstrap_config() -> dict:
    return {
        "team": {
            "members": ["Felipe Santiago"],
            "roles_confirmed": True,
            "assignments": {
                role: "Felipe Santiago"
                for role in REQUIRED_TEAM_ASSIGNMENTS
            },
        },
        "style": {
            "name": "Estilo de teste",
            "trigger_token": "estilo_teste",
            "approval_status": "approved",
        },
        "hugging_face": {
            "namespace": "felipe",
            "token_status": "available_not_versioned",
        },
    }


def checks_by_key(config: dict) -> dict[str, bool]:
    return {check.key: check.ok for check in bootstrap_checks(Path.cwd(), config)}


def test_bootstrap_validates_confirmed_team_assignments() -> None:
    checks = checks_by_key(base_bootstrap_config())

    assert checks["team_roles_confirmed"] is True
    assert checks["team_members"] is True
    assert checks["team_assignments"] is True
    assert checks["team_required_roles"] is True
    assert checks["team_assignment_members"] is True


def test_bootstrap_rejects_missing_required_team_assignments() -> None:
    config = base_bootstrap_config()
    config["team"]["assignments"].pop("avaliacao")

    checks = checks_by_key(config)

    assert checks["team_assignments"] is True
    assert checks["team_required_roles"] is False


def test_bootstrap_rejects_assignees_not_listed_as_members() -> None:
    config = base_bootstrap_config()
    config["team"]["assignments"]["documentacao"] = ["Pessoa Externa"]

    checks = checks_by_key(config)

    assert checks["team_required_roles"] is True
    assert checks["team_assignment_members"] is False


def write_dataset_fixture(root: Path, *, license_value: str = "CC-BY-SA 4.0", size: int = 512) -> None:
    images_dir = root / "dados" / "imagens"
    images_dir.mkdir(parents=True)
    sources_path = root / "dados" / "fontes.csv"
    captions_path = root / "dados" / "legendas.txt"
    sources_path.write_text(
        "arquivo,url,autor,licenca,data_coleta,fonte,observacoes\n"
        + "\n".join(
            f"img_{index:03}.png,https://commons.wikimedia.org/wiki/File:Teste_{index}.png,"
            f"Autor {index},{license_value},2026-07-10,Wikimedia Commons,metadados verificados"
            for index in range(1, 21)
        )
        + "\n",
        encoding="utf-8",
    )
    captions_path.write_text(
        "\n".join(
            f"img_{index:03}.png\tflpxilobr, caption de teste\t" "rascunho"
            for index in range(1, 21)
        )
        + "\n",
        encoding="utf-8",
    )
    for index in range(1, 21):
        Image.new("RGB", (size, size), (246, 240, 222)).save(images_dir / f"img_{index:03}.png")


def dataset_checks_by_key(root: Path) -> dict[str, bool]:
    config = {"style": {"trigger_token": "flpxilobr"}}
    return {check.key: check.ok for check in dataset_checks(root, config)}


def test_dataset_status_accepts_utf8_bom_in_caption_header(tmp_path: Path) -> None:
    write_dataset_fixture(tmp_path)
    captions_path = tmp_path / "dados" / "legendas.txt"
    captions_path.write_text(
        captions_path.read_text(encoding="utf-8").replace("\trascunho", "\trevisada"),
        encoding="utf-8-sig",
    )

    checks = dataset_checks_by_key(tmp_path)

    assert checks["captions_reviewed"] is True


def test_dataset_status_validates_provenance_licenses_and_resolution(tmp_path: Path) -> None:
    write_dataset_fixture(tmp_path)

    checks = dataset_checks_by_key(tmp_path)

    assert checks["image_count"] is True
    assert checks["provenance_count"] is True
    assert checks["provenance_fields"] is True
    assert checks["allowed_licenses"] is True
    assert checks["image_resolution"] is True
    assert checks["captions_reviewed"] is False


def test_dataset_status_rejects_bad_license_and_small_images(tmp_path: Path) -> None:
    write_dataset_fixture(tmp_path, license_value="All rights reserved", size=511)

    checks = dataset_checks_by_key(tmp_path)

    assert checks["allowed_licenses"] is False
    assert checks["image_resolution"] is False
