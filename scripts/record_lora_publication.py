"""Append the verified Hub publication record without rewriting past experiment facts."""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "resultados" / "treino" / "experimentos.csv"
HUB_URL = "https://huggingface.co/RalphError/flpxilobr-lora"


def main() -> None:
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    if any(row.get("status") == "publicado_hub" and row.get("hub_url") == HUB_URL for row in rows):
        print("Publicacao ja registrada.")
        return
    selected = next(row for row in reversed(rows) if row.get("experimento") == "config_b" and row.get("status") == "concluido")
    rows.append({
        **selected,
        "data": datetime.now(UTC).isoformat(),
        "status": "publicado_hub",
        "hub_url": HUB_URL,
        "observacoes": "Pesos selecionados config_b e model card publicados e verificados no Hub.",
    })
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(HUB_URL)


if __name__ == "__main__":
    main()
