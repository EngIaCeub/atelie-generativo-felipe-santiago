from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REQUIRED_DIRS = [
    ".agents/skills",
    ".codex/agents",
    ".github/workflows",
    "app/services",
    "app/tests",
    "config",
    "dados/imagens",
    "docs/runbooks",
    "notebooks",
    "plans/active",
    "plans/completed",
    "relatorio",
    "resultados/treino",
    "resultados/avaliacao",
    "resultados/auditorias",
    "scripts",
    "tests",
]


def migrate_notebooks(root: Path) -> list[str]:
    old = root / "noteboks"
    new = root / "notebooks"
    messages: list[str] = []
    if not old.exists():
        return messages
    if not new.exists():
        old.rename(new)
        messages.append("Renomeado noteboks/ para notebooks/.")
        return messages

    conflicts: list[str] = []
    for source in old.rglob("*"):
        if source.is_dir():
            continue
        relative = source.relative_to(old)
        target = new / relative
        if target.exists():
            conflicts.append(str(relative))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
    if conflicts:
        messages.append("Conflitos não sobrescritos em noteboks/: " + ", ".join(conflicts))
    if not any(old.rglob("*")):
        old.rmdir()
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepara a estrutura do Ateliê Generativo.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()

    messages = migrate_notebooks(root)
    for directory in REQUIRED_DIRS:
        (root / directory).mkdir(parents=True, exist_ok=True)

    print(f"Bootstrap executado em {root}")
    for message in messages:
        print(f"- {message}")
    if not messages:
        print("- Nenhuma migração de noteboks/ necessária.")
    print("- Diretórios mínimos garantidos; arquivos existentes não foram sobrescritos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
