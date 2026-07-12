from __future__ import annotations

import gradio as gr

from app.config import load_config
from app.pipeline import MultimodalPipeline
from app.services.image_generator import LocalLoRAImageGenerator
from app.services.prompt_expander import LocalQwenPromptExpander
from app.services.speech_synthesizer import MMSSpeechSynthesizer

config = load_config()
pipeline = MultimodalPipeline(
    prompt_expander=LocalQwenPromptExpander(config),
    image_generator=LocalLoRAImageGenerator(config),
    speech_synthesizer=MMSSpeechSynthesizer(config),
)


def gerar(tema: str):
    try:
        result = pipeline.run(tema)
        return result.prompt, result.image, result.audio, "Concluido."
    except ValueError as exc:
        return "", None, None, str(exc)
    except Exception:
        return "", None, None, "Nao foi possivel concluir a geracao. Tente novamente em instantes."


demo = gr.Interface(
    fn=gerar,
    inputs=gr.Textbox(label="Tema", placeholder="Ex.: feira de domingo"),
    outputs=[
        gr.Textbox(label="Prompt expandido"),
        gr.Image(label="Imagem"),
        gr.Audio(label="Narracao"),
        gr.Textbox(label="Status"),
    ],
    title="Atelie Generativo - Felipe Santiago",
    description="Descreva um tema do Cerrado para gerar prompt, imagem com LoRA e narracao em portugues.",
)

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=1).launch()
