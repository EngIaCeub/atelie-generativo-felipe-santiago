# ruff: noqa: E402, I001
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import load_config
from app.pipeline import MultimodalPipeline
from app.services.image_generator import LocalLoRAImageGenerator
from app.services.prompt_expander import LocalQwenPromptExpander
from app.services.speech_synthesizer import MMSSpeechSynthesizer

DEFAULT_THEMES = [
    "lobo-guara entre capim dourado",
    "seriema ao amanhecer no Cerrado",
    "flores de pequi e buritis",
]


def build_pipeline() -> MultimodalPipeline:
    config = load_config()
    return MultimodalPipeline(
        prompt_expander=LocalQwenPromptExpander(config),
        image_generator=LocalLoRAImageGenerator(config),
        speech_synthesizer=MMSSpeechSynthesizer(config),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Executa smoke test real do app multimodal.")
    parser.add_argument("--output-dir", type=Path, default=Path("resultados/app_smoke"))
    parser.add_argument("--themes", nargs="*", default=DEFAULT_THEMES)
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = build_pipeline()
    results = []

    for index, theme in enumerate(args.themes, start=1):
        started = time.perf_counter()
        try:
            result = pipeline.run(theme)
            image_path = output_dir / f"{index:02d}_imagem.png"
            audio_path = output_dir / f"{index:02d}_narracao.wav"
            result.image.save(image_path)
            sample_rate, waveform = result.audio
            sf.write(audio_path, waveform, sample_rate)
            results.append({
                "theme": theme,
                "status": "ok",
                "latency_seconds": round(time.perf_counter() - started, 3),
                "prompt": result.prompt,
                "image": str(image_path),
                "audio": str(audio_path),
            })
        except Exception as exc:
            results.append({
                "theme": theme,
                "status": "error",
                "latency_seconds": round(time.perf_counter() - started, 3),
                "error_type": type(exc).__name__,
                "error_message": "Geracao falhou; consulte o console local sem registrar segredos.",
            })

    report = output_dir / "smoke_report.json"
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report)
    return 0 if all(row["status"] == "ok" for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
