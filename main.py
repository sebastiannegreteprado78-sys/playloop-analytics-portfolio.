from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.playloop_analysis import load_data, summarize_metrics, write_summary_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera estadísticas clave para el proyecto PlayLoop.")
    parser.add_argument(
        "--folder",
        type=str,
        default="/content/drive/MyDrive/playloop_datasets (1)",
        help="Ruta a la carpeta con los CSV del proyecto.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/summary.csv",
        help="Ruta donde guardar el resumen ejecutivo en CSV.",
    )
    args = parser.parse_args()

    data = load_data(args.folder)
    metrics = summarize_metrics(data["usuarios"], data["sesiones"], data["compras"])

    write_summary_csv(metrics, args.output)

    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
