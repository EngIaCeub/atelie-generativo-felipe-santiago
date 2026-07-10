from __future__ import annotations

import gradio as gr

from app.pipeline import MultimodalPipeline
from app.services.image_generator import PendingImageGenerator
from app.services.prompt_expander import PendingPromptExpander
from app.services.speech_synthesizer import PendingSpeechSynthesizer

pipeline = MultimodalPipeline(
    prompt_expander=PendingPromptExpander(),
    image_generator=PendingImageGenerator(),
    speech_synthesizer=PendingSpeechSynthesizer(),
)


def gerar(tema: str):
    try:
        result = pipeline.run(tema)
        return result.prompt, result.image, result.audio, "Concluído."
    except Exception as exc:  # mensagem controlada para scaffold; revisar antes da publicação
        return "", None, None, f"Aplicação ainda não configurada: {exc}"


demo = gr.Interface(
    fn=gerar,
    inputs=gr.Textbox(label="Tema", placeholder="Ex.: feira de domingo"),
    outputs=[
        gr.Textbox(label="Prompt expandido"),
        gr.Image(label="Imagem"),
        gr.Audio(label="Narração"),
        gr.Textbox(label="Status"),
    ],
    title="Ateliê Generativo — Felipe Santiago",
    description="Scaffold: configure os três backends antes de publicar.",
)

if __name__ == "__main__":
    demo.queue().launch()
