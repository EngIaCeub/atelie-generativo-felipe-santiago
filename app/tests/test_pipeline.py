from __future__ import annotations

import pytest

from app.config import load_config
from app.pipeline import MultimodalPipeline
from app.services.image_generator import LocalLoRAImageGenerator
from app.services.prompt_expander import LocalQwenPromptExpander


class Prompt:
    def expand(self, theme: str) -> str:
        return f"estilo_teste, {theme}"


class Image:
    def generate(self, prompt: str) -> str:
        return f"imagem:{prompt}"


class Speech:
    def synthesize(self, text: str) -> str:
        return f"audio:{text}"


def test_pipeline_contract() -> None:
    pipeline = MultimodalPipeline(Prompt(), Image(), Speech())
    result = pipeline.run(" feira ")
    assert result.prompt == "estilo_teste, feira"
    assert result.image.startswith("imagem:")
    assert result.audio.startswith("audio:")


def test_pipeline_rejects_empty_theme() -> None:
    pipeline = MultimodalPipeline(Prompt(), Image(), Speech())
    with pytest.raises(ValueError):
        pipeline.run("   ")


def test_real_providers_use_project_configuration() -> None:
    config = load_config()
    assert config.style_token == "flpxilobr"
    assert config.lora_weights_path.name == "pytorch_lora_weights.safetensors"
    assert config.tts_model_id == "facebook/mms-tts-por"


def test_prompt_expander_preserves_style_token_without_loading_model() -> None:
    config = load_config()
    expander = LocalQwenPromptExpander(config)
    assert expander.config.style_token == "flpxilobr"
    assert expander._model is None


def test_prompt_expander_falls_back_when_llm_response_is_not_portuguese_or_on_theme() -> None:
    expander = LocalQwenPromptExpander(load_config())
    prompt = expander._format_prompt("seriema ao amanhecer no Cerrado", "flpxilobr, Flowers with effects")
    assert prompt.startswith("flpxilobr, seriema ao amanhecer no Cerrado")
    assert "hachuras artesanais" in prompt


def test_image_provider_uses_local_lora_weights_first() -> None:
    provider = LocalLoRAImageGenerator(load_config())
    assert provider._resolve_weights().exists()
