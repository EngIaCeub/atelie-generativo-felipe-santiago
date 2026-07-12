from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    style_token: str
    lora_repo_id: str
    base_model_id: str
    prompt_model_id: str
    tts_model_id: str
    lora_weights_path: Path
    hf_token_available: bool
    app_mode: str


def load_config() -> AppConfig:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "config" / "project.json").read_text(encoding="utf-8"))
    training_weights = root / "resultados" / "treino" / "local" / "config_b" / "pytorch_lora_weights.safetensors"
    bundled_weights = root / "lora" / "pytorch_lora_weights.safetensors"
    default_weights = training_weights if training_weights.exists() else bundled_weights
    return AppConfig(
        style_token=data["style"]["trigger_token"],
        lora_repo_id=os.environ.get("HF_LORA_REPO", data["hugging_face"]["lora_repo_id"]),
        base_model_id=os.environ.get("BASE_MODEL_ID", data["models"]["base_diffusion"]),
        prompt_model_id=os.environ.get("PROMPT_MODEL_ID", data["models"]["prompt_expander"]),
        tts_model_id=os.environ.get("TTS_MODEL_ID", data["models"]["tts"]),
        lora_weights_path=Path(os.environ.get(
            "LORA_WEIGHTS_PATH",
            default_weights,
        )),
        hf_token_available=bool(os.environ.get("HF_TOKEN")),
        app_mode=os.environ.get("APP_MODE", "development"),
    )
