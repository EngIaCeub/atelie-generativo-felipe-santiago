# Atelie Generativo - treino LoRA no Colab
#
# Cole/execute esta celula em um runtime Colab com GPU.
# O token HF deve existir em Secrets como HF_TOKEN. O valor nunca e impresso.

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from google.colab import drive, userdata


PROJECT_REPO_URL = "https://github.com/EngIaCeub/atelie-generativo-felipe-santiago.git"
WORK_ROOT = Path("/content/atelie_generativo_work")
PROJECT_DIR = WORK_ROOT / "repo"
DIFFUSERS_DIR = WORK_ROOT / "diffusers"
DATASET_DIR = WORK_ROOT / "dataset_flpxilobr"
DRIVE_ROOT = Path("/content/drive/MyDrive/atelie_generativo_felipe_santiago")
LOCAL_FALLBACK_ROOT = Path("/content/atelie_generativo_outputs")
OUTPUT_ROOT = DRIVE_ROOT / "treino_lora"
EXPERIMENTS_CSV = OUTPUT_ROOT / "experimentos_colab.csv"


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def run_capture(cmd: list[str], cwd: Path | None = None) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd) if cwd else None, text=True).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dataset_hash(dataset_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(dataset_dir.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(dataset_dir).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(sha256_file(path).encode("ascii"))
            digest.update(b"\0")
    return digest.hexdigest()


def append_experiment(row: dict[str, object]) -> None:
    fieldnames = [
        "experimento",
        "data",
        "commit",
        "diffusers_commit",
        "dataset_hash",
        "seed",
        "rank",
        "learning_rate",
        "max_train_steps",
        "status",
        "checkpoint",
        "hub_url",
        "observacoes",
    ]
    EXPERIMENTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    exists = EXPERIMENTS_CSV.exists()
    with EXPERIMENTS_CSV.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({name: row.get(name, "") for name in fieldnames})


def configure_output_root() -> str:
    global OUTPUT_ROOT, EXPERIMENTS_CSV

    print("Montando Google Drive para checkpoints...")
    try:
        drive.mount("/content/drive", force_remount=True)
        OUTPUT_ROOT = DRIVE_ROOT / "treino_lora"
        persistence_note = "checkpoints no Google Drive"
    except Exception as exc:
        OUTPUT_ROOT = LOCAL_FALLBACK_ROOT / "treino_lora"
        persistence_note = (
            "Drive indisponivel; checkpoints em /content, temporarios. "
            f"Erro real: {type(exc).__name__}: {exc}"
        )
        print("AVISO:", persistence_note)

    EXPERIMENTS_CSV = OUTPUT_ROOT / "experimentos_colab.csv"
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    return persistence_note


def prepare_environment() -> tuple[dict, str, str, str, str]:
    print("Verificando token Hugging Face sem exibir valor...")
    hf_token = userdata.get("HF_TOKEN") or os.environ.get("HF_TOKEN")
    assert hf_token, "HF_TOKEN nao encontrado em Secrets/ambiente do Colab."
    os.environ["HF_TOKEN"] = hf_token
    os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token

    print("Instalando dependencias oficiais do exemplo Diffusers...")
    run([sys.executable, "-m", "pip", "install", "-q", "--upgrade", "pip"])
    if not DIFFUSERS_DIR.exists():
        run(["git", "clone", "--depth", "1", "https://github.com/huggingface/diffusers.git", str(DIFFUSERS_DIR)])
    else:
        run(["git", "pull", "--ff-only"], cwd=DIFFUSERS_DIR)
    diffusers_commit = run_capture(["git", "rev-parse", "HEAD"], cwd=DIFFUSERS_DIR)
    run([sys.executable, "-m", "pip", "install", "-q", "-e", str(DIFFUSERS_DIR)])
    run([sys.executable, "-m", "pip", "install", "-q", "-r", str(DIFFUSERS_DIR / "examples/text_to_image/requirements.txt")])
    run([sys.executable, "-m", "pip", "install", "-q", "peft", "safetensors", "huggingface_hub", "tensorboard"])

    print("Configurando Accelerate...")
    run(["accelerate", "config", "default", "--mixed_precision", "fp16"])

    print("Verificando GPU...")
    try:
        run(["nvidia-smi"])
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Runtime Colab sem GPU ativa. Altere para GPU/T4 antes de treinar.") from exc

    persistence_note = configure_output_root()

    print("Clonando/atualizando repositorio do projeto...")
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    if not PROJECT_DIR.exists():
        run(["git", "clone", PROJECT_REPO_URL, str(PROJECT_DIR)])
    else:
        run(["git", "pull", "--ff-only"], cwd=PROJECT_DIR)
    project_commit = run_capture(["git", "rev-parse", "HEAD"], cwd=PROJECT_DIR)

    config = json.loads((PROJECT_DIR / "config/project.json").read_text(encoding="utf-8"))
    from huggingface_hub import login

    login(token=hf_token, add_to_git_credential=False)
    return config, project_commit, diffusers_commit, hf_token, persistence_note


def prepare_dataset(project_dir: Path) -> str:
    print("Preparando dataset imagefolder a partir de dados/metadata.jsonl...")
    metadata_path = project_dir / "dados/metadata.jsonl"
    records = [json.loads(line) for line in metadata_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert 20 <= len(records) <= 40, f"Quantidade invalida de registros: {len(records)}"

    if DATASET_DIR.exists():
        shutil.rmtree(DATASET_DIR)
    DATASET_DIR.mkdir(parents=True)

    rewritten = []
    for record in records:
        source = project_dir / record["file_name"]
        assert source.exists(), f"Imagem ausente: {source}"
        assert record["text"].startswith("flpxilobr,"), f"Caption sem token: {source.name}"
        target = DATASET_DIR / source.name
        shutil.copy2(source, target)
        rewritten.append({"file_name": target.name, "text": record["text"]})

    with (DATASET_DIR / "metadata.jsonl").open("w", encoding="utf-8") as handle:
        for record in rewritten:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    digest = dataset_hash(DATASET_DIR)
    print(f"Dataset preparado: {len(rewritten)} imagens; hash={digest}")
    return digest


def run_training(config: dict, project_commit: str, diffusers_commit: str, digest: str, persistence_note: str) -> None:
    script = DIFFUSERS_DIR / "examples/text_to_image/train_text_to_image_lora.py"
    assert script.exists(), f"Script oficial ausente: {script}"

    training = config["training"]
    base_model = config["models"]["base_diffusion"]
    seed = str(training["seed"])
    resolution = str(training["resolution"])

    for cfg in training["configs"]:
        name = cfg["name"]
        output_dir = OUTPUT_ROOT / name
        output_dir.mkdir(parents=True, exist_ok=True)
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        checkpoint = ""
        status = "started"
        notes = f"Treino iniciado no Colab; push_to_hub desativado ate escolha da melhor configuracao; {persistence_note}."
        append_experiment(
            {
                "experimento": name,
                "data": started,
                "commit": project_commit,
                "diffusers_commit": diffusers_commit,
                "dataset_hash": digest,
                "seed": seed,
                "rank": cfg["rank"],
                "learning_rate": cfg["learning_rate"],
                "max_train_steps": cfg["max_train_steps"],
                "status": status,
                "checkpoint": "",
                "hub_url": "",
                "observacoes": notes,
            }
        )

        cmd = [
            "accelerate",
            "launch",
            str(script),
            "--pretrained_model_name_or_path",
            base_model,
            "--train_data_dir",
            str(DATASET_DIR),
            "--image_column",
            "image",
            "--caption_column",
            "text",
            "--resolution",
            resolution,
            "--center_crop",
            "--random_flip",
            "--train_batch_size",
            "1",
            "--gradient_accumulation_steps",
            "4",
            "--max_train_steps",
            str(cfg["max_train_steps"]),
            "--learning_rate",
            str(cfg["learning_rate"]),
            "--lr_scheduler",
            "constant",
            "--lr_warmup_steps",
            "0",
            "--rank",
            str(cfg["rank"]),
            "--checkpointing_steps",
            "250",
            "--checkpoints_total_limit",
            "3",
            "--resume_from_checkpoint",
            "latest",
            "--seed",
            seed,
            "--mixed_precision",
            "fp16",
            "--validation_prompt",
            "flpxilobr, um lobo-guara no Cerrado em xilogravura digital",
            "--num_validation_images",
            "2",
            "--validation_epochs",
            "1",
            "--output_dir",
            str(output_dir),
            "--report_to",
            "tensorboard",
        ]

        try:
            run(cmd)
            checkpoints = sorted(output_dir.glob("checkpoint-*"))
            checkpoint = str(checkpoints[-1]) if checkpoints else str(output_dir)
            status = "concluido"
            notes = f"Treino concluido no Colab; revisar imagens de validacao antes de publicar no Hub; {persistence_note}."
        except Exception as exc:
            status = "falhou"
            notes = f"Falha real registrada no Colab: {type(exc).__name__}: {exc}"
            raise
        finally:
            append_experiment(
                {
                    "experimento": name,
                    "data": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "commit": project_commit,
                    "diffusers_commit": diffusers_commit,
                    "dataset_hash": digest,
                    "seed": seed,
                    "rank": cfg["rank"],
                    "learning_rate": cfg["learning_rate"],
                    "max_train_steps": cfg["max_train_steps"],
                    "status": status,
                    "checkpoint": checkpoint,
                    "hub_url": "",
                    "observacoes": notes,
                }
            )


config, project_commit, diffusers_commit, _hf_token, persistence_note = prepare_environment()
digest = prepare_dataset(PROJECT_DIR)
run_training(config, project_commit, diffusers_commit, digest, persistence_note)
print(f"Treinos finalizados. Evidencia CSV neste runtime: {EXPERIMENTS_CSV}")
