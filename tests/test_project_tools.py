from __future__ import annotations

import json
from pathlib import Path

from scripts.check_secrets import scan
from scripts.project_status import REQUIRED_TEAM_ASSIGNMENTS, bootstrap_checks, collect


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
