import pandas as pd

from src.playloop_analysis import summarize_metrics


def test_summarize_metrics_basic_totals():
    users = pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4],
            "plataforma": ["ios", "android", "ios", "android"],
            "pais": ["MX", "US", "MX", "BR"],
        }
    )
    sessions = pd.DataFrame(
        {
            "evento_id": [10, 11, 12, 13],
            "duracion_segundos": [120, 300, 180, 240],
            "fecha": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02"],
            "plataforma": ["ios", "android", "ios", "android"],
        }
    )
    purchases = pd.DataFrame(
        {
            "compra_id": [1, 2, 3],
            "producto_id": [101, 102, 101],
            "importe": ["€10", "$20.50", "€15"],
            "reembolso": [0, 0, 1],
            "fecha": ["2024-01-01", "2024-01-01", "2024-01-02"],
            "plataforma": ["ios", "android", "ios"],
        }
    )

    metrics = summarize_metrics(users, sessions, purchases)

    assert metrics["total_users"] == 4
    assert metrics["total_sessions"] == 4
    assert metrics["total_revenue"] == 30.5
    assert metrics["avg_session_duration"] == 210.0
    assert metrics["platform_share"]["iOS"] == 2
    assert metrics["platform_share"]["Android"] == 2


def test_summarize_metrics_handles_missing_values_and_currency():
    users = pd.DataFrame(
        {
            "user_id": [1, 2, None],
            "plataforma": ["ios", "", "android"],
            "pais": ["mx", "US", None],
        }
    )
    sessions = pd.DataFrame(
        {
            "evento_id": [1, 2],
            "duracion_segundos": [None, 90],
            "fecha": ["2024-01-01", "2024-01-01"],
            "plataforma": ["ios", "android"],
        }
    )
    purchases = pd.DataFrame(
        {
            "compra_id": [1, 2],
            "producto_id": [101, 103],
            "importe": ["€5", "€7,50"],
            "reembolso": [0, 0],
            "fecha": ["2024-01-01", "2024-01-01"],
            "plataforma": ["ios", "android"],
        }
    )

    metrics = summarize_metrics(users, sessions, purchases)

    assert metrics["total_users"] == 2
    assert metrics["avg_session_duration"] == 90.0
    assert metrics["total_revenue"] == 12.5
    assert metrics["country_share"]["MX"] == 1
