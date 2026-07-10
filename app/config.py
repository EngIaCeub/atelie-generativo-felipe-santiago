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
    hf_token_available: bool
    app_mode: str


def load_config() -> AppConfig:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "config" / "project.json").read_text(encoding="utf-8"))
    return AppConfig(
        style_token=data["style"]["trigger_token"],
        lora_repo_id=data["hugging_face"]["lora_repo_id"],
        base_model_id=data["models"]["base_diffusion"],
        prompt_model_id=data["models"]["prompt_expander"],
        tts_model_id=data["models"]["tts"],
        hf_token_available=bool(os.environ.get("HF_TOKEN")),
        app_mode=os.environ.get("APP_MODE", "development"),
    )
