from __future__ import annotations

import numpy as np
import torch

from app.config import AppConfig


class MMSSpeechSynthesizer:
    """Sintetiza audio em portugues com o modelo MMS-TTS."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._model = None
        self._tokenizer = None

    def _load(self) -> None:
        if self._model is not None:
            return
        from transformers import AutoTokenizer, VitsModel

        self._tokenizer = AutoTokenizer.from_pretrained(self.config.tts_model_id)
        self._model = VitsModel.from_pretrained(self.config.tts_model_id)
        self._model.eval()

    def synthesize(self, text: str) -> tuple[int, np.ndarray]:
        self._load()
        assert self._model is not None and self._tokenizer is not None
        inputs = self._tokenizer(text[:500], return_tensors="pt")
        with torch.inference_mode():
            waveform = self._model(**inputs).waveform.squeeze().cpu().numpy()
        return int(self._model.config.sampling_rate), waveform
