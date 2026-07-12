"""Apply the Colab portability layer to the two academic notebooks."""

from __future__ import annotations

from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/EngIaCeub/atelie-generativo-felipe-santiago.git"

BOOTSTRAP = f'''# Colab bootstrap: run this cell first in a clean GPU runtime.
import os
import subprocess
from pathlib import Path

IN_COLAB = True
PROJECT_REPO_URL = "{REPO_URL}"
COLAB_ROOT = Path("/content/atelie_generativo")
PROJECT_DIR = COLAB_ROOT / "repo"
subprocess.run(["nvidia-smi"], check=True)
subprocess.run(["git", "clone", PROJECT_REPO_URL, str(PROJECT_DIR)] if not PROJECT_DIR.exists() else ["git", "-C", str(PROJECT_DIR), "pull", "--ff-only"], check=True)
os.chdir(PROJECT_DIR)
try:
    from google.colab import drive, userdata
    drive.mount("/content/drive", force_remount=False)
    token = userdata.get("HF_TOKEN") or os.environ.get("HF_TOKEN")
    if token:
        os.environ["HF_TOKEN"] = token
        os.environ["HUGGING_FACE_HUB_TOKEN"] = token
except ImportError:
    raise RuntimeError("Este notebook deve ser executado no Google Colab.")
print("Projeto Colab:", PROJECT_DIR)
'''


def first_code_index(doc: nbformat.NotebookNode) -> int:
    return next(index for index, cell in enumerate(doc.cells) if cell.cell_type == "code")


def adapt_training(path: Path) -> None:
    doc = nbformat.read(path, as_version=4)
    doc.cells.insert(first_code_index(doc), nbformat.v4.new_code_cell(BOOTSTRAP))
    for cell in doc.cells:
        if cell.cell_type != "code":
            continue
        source = cell.source
        source = source.replace('NOTEBOOK_REVISION = "local-nvidia-gpu-2026-07-11-v7"', 'NOTEBOOK_REVISION = "colab-gpu-2026-07-11-v1"')
        source = source.replace("RUN_TRAINING = True", "RUN_TRAINING = False  # Mude para True para iniciar o treino real.")
        source = source.replace("INSTALL_LOCAL_DEPS = False", "INSTALL_LOCAL_DEPS = False")
        source = source.replace('OUTPUT_ROOT = ROOT / "resultados/treino/local"', 'OUTPUT_ROOT = Path("/content/drive/MyDrive/atelie_generativo_felipe_santiago/treino_lora")')
        source = source.replace('DIFFUSERS_DIR = Path(r"C:\\ag-diffusers")', 'DIFFUSERS_DIR = Path("/content/atelie_generativo/diffusers")')
        source = source.replace('EXPERIMENTS_CSV = ROOT / "resultados/treino/experimentos.csv"', 'EXPERIMENTS_CSV = OUTPUT_ROOT / "experimentos_colab.csv"')
        source = source.replace('EXPECTED_VENV = ROOT / ".venv" / "Scripts" / "python.exe"', 'EXPECTED_VENV = Path("/content")')
        source = source.replace('Instalacao local de PyTorch CUDA desativada', 'Instalacao adicional de PyTorch desativada (o Colab ja fornece CUDA)')
        cell.source = source
    doc.cells[0].source = "# 02 - Fine-tuning LoRA no Google Colab\n\nNotebook executavel em Colab limpo com GPU. Os checkpoints sao persistidos no Google Drive; o token e lido apenas de Secret/ambiente e nunca exibido."
    nbformat.write(doc, path)


def adapt_evaluation(path: Path) -> None:
    doc = nbformat.read(path, as_version=4)
    doc.cells.insert(first_code_index(doc), nbformat.v4.new_code_cell(BOOTSTRAP))
    for cell in doc.cells:
        if cell.cell_type != "code":
            continue
        source = cell.source
        source = source.replace('NOTEBOOK_REVISION = "evaluation-local-2026-07-11-v1"', 'NOTEBOOK_REVISION = "evaluation-colab-2026-07-11-v1"')
        source = source.replace('RESULTS_DIR = ROOT / "resultados/avaliacao"', 'RESULTS_DIR = Path("/content/drive/MyDrive/atelie_generativo_felipe_santiago/avaliacao_colab")')
        source = source.replace('LORA_DIR = ROOT / "resultados/treino/local" / SELECTED_LORA_CONFIG\nLORA_WEIGHTS = LORA_DIR / "pytorch_lora_weights.safetensors"', 'from huggingface_hub import hf_hub_download\n_hub_config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))\nLORA_WEIGHTS = Path(hf_hub_download(_hub_config["hugging_face"]["lora_repo_id"], "pytorch_lora_weights.safetensors", token=os.environ.get("HF_TOKEN")))\nLORA_DIR = LORA_WEIGHTS.parent')
        source = source.replace('from huggingface_hub import hf_hub_download\nLORA_WEIGHTS = Path(hf_hub_download(config["hugging_face"]["lora_repo_id"], "pytorch_lora_weights.safetensors", token=os.environ.get("HF_TOKEN")))\nLORA_DIR = LORA_WEIGHTS.parent', 'from huggingface_hub import hf_hub_download\n_hub_config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))\nLORA_WEIGHTS = Path(hf_hub_download(_hub_config["hugging_face"]["lora_repo_id"], "pytorch_lora_weights.safetensors", token=os.environ.get("HF_TOKEN")))\nLORA_DIR = LORA_WEIGHTS.parent')
        source = source.replace('Pesos LoRA: c:\\\\Users\\\\felip', 'Pesos LoRA publicados no Hub:')
        cell.source = source
    doc.cells[0].source = "# 03 - Avaliacao base x LoRA no Google Colab\n\nNotebook executavel em Colab limpo com GPU. Ele baixa os pesos publicados no Hub e salva evidencias novas no Google Drive, sem substituir a entrega local."
    nbformat.write(doc, path)


def main() -> None:
    adapt_training(ROOT / "notebooks" / "02_treino_lora.ipynb")
    adapt_evaluation(ROOT / "notebooks" / "03_avaliacao.ipynb")
    print("Notebooks adaptados para Colab.")


if __name__ == "__main__":
    main()
