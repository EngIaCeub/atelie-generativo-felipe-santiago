from __future__ import annotations

import torch

from app.config import AppConfig


class LocalQwenPromptExpander:
    """Expande o tema com Qwen, carregado somente na primeira solicitacao."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._model = None
        self._tokenizer = None

    def _load(self) -> None:
        if self._model is not None:
            return
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._tokenizer = AutoTokenizer.from_pretrained(self.config.prompt_model_id)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.config.prompt_model_id,
            torch_dtype=torch.float32,
        )
        # Reserva a VRAM da RTX 3050 para a inferencia Stable Diffusion.
        self._model.to("cpu")
        self._model.eval()

    def expand(self, theme: str) -> str:
        self._load()
        assert self._model is not None and self._tokenizer is not None
        messages = [
            {
                "role": "system",
                "content": (
                    "Retorne somente um prompt de imagem em uma unica frase, com 25 a 45 palavras, em "
                    "portugues. Comece com flpxilobr, descreva apenas elementos visuais do tema, composicao, "
                    "alto contraste e hachuras de xilogravura digital. Nao use listas, titulos, explicacoes, "
                    "termos em ingles, nomes de artistas, personagens protegidos, camera ou instrucoes de edicao."
                ),
            },
            {"role": "user", "content": f"Tema: {theme}"},
        ]
        rendered = self._tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        device = next(self._model.parameters()).device
        inputs = self._tokenizer(rendered, return_tensors="pt").to(device)
        with torch.inference_mode():
            generated = self._model.generate(**inputs, max_new_tokens=64, do_sample=False)
        text = self._tokenizer.decode(generated[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
        text = " ".join(text.split()).strip()
        return self._format_prompt(theme, text)

    def _format_prompt(self, theme: str, generated: str) -> str:
        """Mantem o contrato visual quando o modelo pequeno responde em idioma ou formato inadequado."""
        normalized = generated.strip()
        words = normalized.lower().replace(",", " ").split()
        theme_words = [word for word in theme.lower().replace("-", " ").split() if len(word) > 3]
        english_markers = {"flowers", "digital", "with", "and", "high", "effects"}
        valid = (
            normalized.startswith(self.config.style_token + ",")
            and 12 <= len(words) <= 55
            and any(word in words for word in theme_words)
            and not english_markers.intersection(words)
        )
        if valid:
            return normalized
        return (
            f"{self.config.style_token}, {theme}, composicao equilibrada do Cerrado, "
            "contornos pretos marcantes, alto contraste, hachuras artesanais e paleta reduzida "
            "em preto e marfim, xilogravura digital"
        )
