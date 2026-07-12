from __future__ import annotations

import argparse
import json
from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Cria e envia o bundle do Hugging Face Space autorizado.")
    parser.add_argument("--bundle", type=Path, default=ROOT / "space")
    args = parser.parse_args()
    config = json.loads((ROOT / "config" / "project.json").read_text(encoding="utf-8"))
    repo_id = config["hugging_face"]["space_repo_id"]
    bundle = args.bundle.resolve()
    if not (bundle / "app.py").exists():
        raise FileNotFoundError(f"Bundle ausente ou invalido: {bundle}")

    api = HfApi()
    api.whoami()
    repo = api.create_repo(repo_id, repo_type="space", space_sdk="gradio", private=False, exist_ok=True)
    commit = api.upload_folder(
        repo_id=repo_id,
        repo_type="space",
        folder_path=bundle,
        ignore_patterns=["**/__pycache__/**", "**/*.pyc"],
        commit_message="Publica app multimodal com LoRA config_b",
    )
    info = api.space_info(repo_id)
    print(json.dumps({
        "repo_url": str(repo),
        "commit_oid": commit.oid,
        "runtime_stage": getattr(info.runtime, "stage", None) if info.runtime else None,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
