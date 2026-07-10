from __future__ import annotations


class PendingSpeechSynthesizer:
    """Marcador explícito: escolher TTS adequado a português e ao Space gratuito."""

    def synthesize(self, text: str):
        raise RuntimeError("Backend de TTS ainda não configurado.")
