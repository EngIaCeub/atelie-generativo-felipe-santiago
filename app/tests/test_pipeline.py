from __future__ import annotations

import pytest

from app.pipeline import MultimodalPipeline


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
