from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.project_status import collect

STAGES = ["bootstrap", "dataset", "training", "evaluation", "publication", "final"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida requisitos cumulativos até um estágio.")
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    all_checks = collect(args.root.resolve())
    last = STAGES.index(args.stage)
    failures = []
    for stage in STAGES[: last + 1]:
        for check in all_checks[stage]:
            if not check.ok:
                failures.append((stage, check.key, check.message))
    if failures:
        print(f"Validação '{args.stage}' falhou com {len(failures)} pendência(s):")
        for stage, key, message in failures:
            print(f"- [{stage}] {key}: {message}")
        return 1
    print(f"Validação '{args.stage}' aprovada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
