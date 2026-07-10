from __future__ import annotations


class PendingPromptExpander:
    """Marcador explícito: Codex deve substituir por backend real e testado."""

    def expand(self, theme: str) -> str:
        raise RuntimeError("Backend de expansão de prompt ainda não configurado.")
