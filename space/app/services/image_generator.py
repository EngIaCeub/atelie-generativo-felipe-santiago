from __future__ import annotations

import os
from pathlib import Path

import torch

from app.config import AppConfig


class LocalLoRAImageGenerator:
    """Gera imagens com Stable Diffusion e carrega explicitamente os pesos LoRA."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._pipeline = None

    def _resolve_weights(self) -> Path:
        if self.config.lora_weights_path.exists():
            return self.config.lora_weights_path
        from huggingface_hub import hf_hub_download

        downloaded = hf_hub_download(
            repo_id=self.config.lora_repo_id,
            filename="pytorch_lora_weights.safetensors",
            token=os.environ.get("HF_TOKEN") or None,
        )
        return Path(downloaded)

    def _load(self) -> None:
        if self._pipeline is not None:
            return
        from diffusers import DPMSolverMultistepScheduler, StableDiffusionPipeline

        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        token = os.environ.get("HF_TOKEN") or None
        self._pipeline = StableDiffusionPipeline.from_pretrained(
            self.config.base_model_id,
            torch_dtype=dtype,
            token=token,
            safety_checker=None,
            requires_safety_checker=False,
        )
        self._pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self._pipeline.scheduler.config)
        weights = self._resolve_weights()
        self._pipeline.load_lora_weights(str(weights.parent), weight_name=weights.name)
        self._pipeline.enable_attention_slicing()
        self._pipeline.to(device)

    def generate(self, prompt: str):
        self._load()
        assert self._pipeline is not None
        device = "cuda" if torch.cuda.is_available() else "cpu"
        seed = int(os.environ.get("APP_SEED", "2026"))
        default_steps = "30" if device == "cuda" else "12"
        inference_steps = int(os.environ.get("APP_INFERENCE_STEPS", default_steps))
        generator = torch.Generator(device=device).manual_seed(seed)
        return self._pipeline(
            prompt=prompt,
            negative_prompt="low quality, blurry, watermark, signature, text, logo",
            width=512,
            height=512,
            num_inference_steps=inference_steps,
            guidance_scale=7.5,
            generator=generator,
        ).images[0]
