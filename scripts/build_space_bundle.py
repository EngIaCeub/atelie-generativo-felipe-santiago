from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_APP = ROOT / "app"
SOURCE_CONFIG = ROOT / "config" / "project.json"
SOURCE_WEIGHTS = ROOT / "resultados" / "treino" / "local" / "config_b" / "pytorch_lora_weights.safetensors"

README = """---
title: Atelie Generativo - Xilogravura do Cerrado
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 6.20.0
python_version: 3.11
app_file: app.py
pinned: false
---

# Atelie Generativo

Informe um tema do Cerrado para gerar um prompt, uma imagem com LoRA e uma narracao em portugues.

O Space usa Stable Diffusion v1.5 com os pesos LoRA incluidos neste repositorio. O token, quando necessario para baixar o modelo base, deve existir somente nos Secrets do Space.
"""

ENTRYPOINT = """from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

package_dir = Path(__file__).resolve().parent / "app"
spec = importlib.util.spec_from_file_location(
    "app",
    package_dir / "__init__.py",
    submodule_search_locations=[str(package_dir)],
)
if spec is None or spec.loader is None:
    raise RuntimeError("Pacote da aplicacao ausente.")
package = importlib.util.module_from_spec(spec)
sys.modules["app"] = package
spec.loader.exec_module(package)

from app.app import demo

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=1).launch()
"""


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser(description="Monta bundle autocontido para Hugging Face Space.")
    parser.add_argument("--output", type=Path, default=ROOT / "space")
    args = parser.parse_args()
    output = args.output.resolve()

    if output.exists():
        raise FileExistsError(f"Bundle ja existe: {output}. Remova-o conscientemente antes de reconstruir.")
    if not SOURCE_WEIGHTS.exists():
        raise FileNotFoundError(f"Pesos LoRA ausentes: {SOURCE_WEIGHTS}")
    output.mkdir(parents=True)
    shutil.copytree(SOURCE_APP, output / "app", ignore=shutil.ignore_patterns("__pycache__", "tests"))
    (output / "app" / "__init__.py").write_text("", encoding="utf-8")
    copy_file(SOURCE_CONFIG, output / "config" / "project.json")
    copy_file(SOURCE_WEIGHTS, output / "lora" / SOURCE_WEIGHTS.name)
    copy_file(SOURCE_APP / "requirements.txt", output / "requirements.txt")
    (output / "app.py").write_text(ENTRYPOINT, encoding="utf-8")
    (output / "README.md").write_text(README, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
