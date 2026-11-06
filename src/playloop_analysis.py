from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def normalize_platform(series: pd.Series) -> pd.Series:
    """Standardizes platform names to the same casing used in the dashboard."""
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .replace({"ios": "iOS", "android": "Android"})
    )


def clean_currency(value: Any) -> float:
    """Converts strings like '€10', '$20.50' or '€7,50' into numeric values."""
    if pd.isna(value):
        return 0.0

    text = str(value).strip()
    text = text.replace("€", "").replace("$", "")
    text = text.replace(".", "").replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return 0.0


def load_data(folder_path: str | Path) -> dict[str, pd.DataFrame]:
    """Loads the seven source tables expected for this project."""
    folder = Path(folder_path)
    required = [
        "compras.csv",
        "gasto_ua.csv",
        "ingresos_ads.csv",
        "partidas.csv",
        "productos_iap.csv",
        "usuarios.csv",
        "sesiones.csv",
    ]

    missing = [name for name in required if not (folder / name).exists()]
    if missing:
        raise FileNotFoundError(f"Faltan los archivos esperados en {folder}: {missing}")

    return {
        "compras": pd.read_csv(folder / "compras.csv"),
        "gasto_ua": pd.read_csv(folder / "gasto_ua.csv"),
        "ingresos_ads": pd.read_csv(folder / "ingresos_ads.csv"),
        "partidas": pd.read_csv(folder / "partidas.csv"),
        "productos_iap": pd.read_csv(folder / "productos_iap.csv"),
        "usuarios": pd.read_csv(folder / "usuarios.csv"),
        "sesiones": pd.read_csv(folder / "sesiones.csv"),
    }


def summarize_metrics(
    users: pd.DataFrame,
    sessions: pd.DataFrame,
    purchases: pd.DataFrame,
) -> dict[str, Any]:
    """Builds the core KPI set used by the dashboard."""
    users_clean = users.copy()
    sessions_clean = sessions.copy()
    purchases_clean = purchases.copy()

    if "user_id" in users_clean.columns:
        users_clean["user_id"] = pd.to_numeric(users_clean["user_id"], errors="coerce")
    if "plataforma" in users_clean.columns:
        users_clean["plataforma"] = normalize_platform(users_clean["plataforma"])
    if "pais" in users_clean.columns:
        users_clean["pais"] = users_clean["pais"].astype(str).str.strip().str.upper().replace({"NAN": pd.NA, "NONE": pd.NA})

    if "evento_id" in sessions_clean.columns:
        sessions_clean["evento_id"] = pd.to_numeric(sessions_clean["evento_id"], errors="coerce")
    if "duracion_segundos" in sessions_clean.columns:
        sessions_clean["duracion_segundos"] = pd.to_numeric(sessions_clean["duracion_segundos"], errors="coerce")
    if "plataforma" in sessions_clean.columns:
        sessions_clean["plataforma"] = normalize_platform(sessions_clean["plataforma"])

    if "importe" in purchases_clean.columns:
        purchases_clean["importe_limpio"] = purchases_clean["importe"].apply(clean_currency)
    else:
        purchases_clean["importe_limpio"] = 0.0

    if "reembolso" in purchases_clean.columns:
        purchases_clean["reembolso"] = pd.to_numeric(purchases_clean["reembolso"], errors="coerce").fillna(0)
    else:
        purchases_clean["reembolso"] = 0

    if "plataforma" in purchases_clean.columns:
        purchases_clean["plataforma"] = normalize_platform(purchases_clean["plataforma"])

    valid_purchases = purchases_clean[purchases_clean["reembolso"] == 0].copy()

    total_users = int(users_clean["user_id"].dropna().nunique())
    total_sessions = int(sessions_clean["evento_id"].dropna().nunique())
    total_revenue = float(valid_purchases["importe_limpio"].sum())
    avg_session_duration = float(sessions_clean["duracion_segundos"].dropna().mean()) if "duracion_segundos" in sessions_clean.columns else 0.0

    platform_share = (
        users_clean["plataforma"]
        .dropna()
        .value_counts()
        .sort_index()
        .to_dict()
    )
    country_share = (
        users_clean["pais"]
        .dropna()
        .value_counts()
        .head(10)
        .to_dict()
    )

    if "fecha" in valid_purchases.columns:
        valid_purchases["fecha_dt"] = pd.to_datetime(valid_purchases["fecha"], errors="coerce")
        daily_rev = (
            valid_purchases.groupby(valid_purchases["fecha_dt"].dt.strftime("%Y-%m-%d"))["importe_limpio"]
            .sum()
            .sort_index()
            .to_dict()
        )
    else:
        daily_rev = {}

    if "fecha" in sessions_clean.columns:
        sessions_clean["fecha_dt"] = pd.to_datetime(sessions_clean["fecha"], errors="coerce")
        daily_sessions = (
            sessions_clean.groupby(sessions_clean["fecha_dt"].dt.strftime("%Y-%m-%d"))["evento_id"]
            .count()
            .sort_index()
            .to_dict()
        )
    else:
        daily_sessions = {}

    if "producto_id" in valid_purchases.columns:
        purchased_items = (
            valid_purchases.groupby("producto_id")
            .agg(ventas=("compra_id", "count"), ingresos=("importe_limpio", "sum"))
            .reset_index()
            .to_dict(orient="records")
        )
    else:
        purchased_items = []

    return {
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_revenue": round(total_revenue, 2),
        "avg_session_duration": round(avg_session_duration, 2),
        "platform_share": platform_share,
        "country_share": country_share,
        "daily_rev": daily_rev,
        "daily_sessions": daily_sessions,
        "purchased_items": purchased_items,
    }


def write_summary_csv(metrics: dict[str, Any], output_path: str | Path) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        {"metric": "total_users", "value": metrics.get("total_users", 0)},
        {"metric": "total_sessions", "value": metrics.get("total_sessions", 0)},
        {"metric": "total_revenue", "value": metrics.get("total_revenue", 0.0)},
        {"metric": "avg_session_duration", "value": metrics.get("avg_session_duration", 0.0)},
    ]
    pd.DataFrame(rows).to_csv(output_file, index=False)
