from __future__ import annotations


class PendingImageGenerator:
    """Marcador explícito: a implementação final precisa aplicar o LoRA escolhido."""

    def generate(self, prompt: str):
        raise RuntimeError("Backend de imagem com LoRA ainda não configurado.")
