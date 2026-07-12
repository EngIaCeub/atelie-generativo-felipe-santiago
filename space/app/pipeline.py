from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class PromptExpander(Protocol):
    def expand(self, theme: str) -> str: ...


class ImageGenerator(Protocol):
    def generate(self, prompt: str) -> Any: ...


class SpeechSynthesizer(Protocol):
    def synthesize(self, text: str) -> Any: ...


@dataclass(frozen=True)
class PipelineResult:
    prompt: str
    image: Any
    audio: Any


class MultimodalPipeline:
    def __init__(
        self,
        prompt_expander: PromptExpander,
        image_generator: ImageGenerator,
        speech_synthesizer: SpeechSynthesizer,
    ) -> None:
        self.prompt_expander = prompt_expander
        self.image_generator = image_generator
        self.speech_synthesizer = speech_synthesizer

    def run(self, theme: str) -> PipelineResult:
        clean_theme = theme.strip()
        if not clean_theme:
            raise ValueError("Informe um tema.")
        if len(clean_theme) > 200:
            raise ValueError("O tema deve ter no máximo 200 caracteres.")
        prompt = self.prompt_expander.expand(clean_theme)
        image = self.image_generator.generate(prompt)
        audio = self.speech_synthesizer.synthesize(prompt)
        return PipelineResult(prompt=prompt, image=image, audio=audio)
