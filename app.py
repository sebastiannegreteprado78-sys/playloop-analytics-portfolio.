from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = BASE_DIR / "PlayLoop_Analytics_Report - Reporte_Ejecutivo.csv"


def parse_currency(value):
    if pd.isna(value):
        return 0.0
    text = str(value).strip()
    text = text.replace("€", "").replace("$", "").replace("%", "")
    text = text.replace(".", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0


def load_report(csv_path: str | Path) -> pd.DataFrame:
    data = pd.read_csv(csv_path)
    data.columns = [col.strip() for col in data.columns]

    numeric_columns = [
        "Unidades_Vendidas",
        "Ingresos_EUR",
        "Precio_Unit_Promedio_EUR",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = data[column].apply(parse_currency)

    for column in ["Cuota_Ingresos", "Cuota_Volumen"]:
        if column in data.columns:
            data[column] = data[column].apply(lambda x: parse_currency(x))

    if "ID_Producto" in data.columns:
        data["ID_Producto"] = data["ID_Producto"].astype(str)

    return data.sort_values("Ingresos_EUR", ascending=False).reset_index(drop=True)


st.set_page_config(page_title="PlayLoop Analytics", page_icon="🎮", layout="wide")

st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(135deg, #f3f4ff 0%, #eefaf8 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 {
            color: #1f2a44;
            font-weight: 800;
        }
        .brand-badge {
            display: inline-block;
            background: linear-gradient(135deg, #4f46e5, #10b981);
            color: white;
            border-radius: 999px;
            padding: 0.4rem 0.9rem;
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
            font-weight: 700;
        }
        .insight-box {
            background: rgba(255,255,255,0.75);
            border: 1px solid rgba(79, 70, 229, 0.12);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="brand-badge">Portfolio Analytics</div>', unsafe_allow_html=True)
st.title("PlayLoop Analytics Portfolio")
st.caption("Dashboard ejecutivo de ventas, productividad y monetización de contenido IAP")

with st.sidebar:
    st.header("Acciones")
    uploaded_file = st.file_uploader("Subir CSV", type=["csv"])
    st.markdown("---")
    st.caption("Proyecto pensado para presentar en entrevistas, portfolios y demos de negocio.")

if uploaded_file is not None:
    df = load_report(uploaded_file)
else:
    df = load_report(DEFAULT_CSV)

if df.empty:
    st.warning("No se encontraron filas en el archivo CSV cargado.")
    st.stop()

total_units = int(df["Unidades_Vendidas"].sum())
total_revenue = float(df["Ingresos_EUR"].sum())
avg_unit_price = float(df["Precio_Unit_Promedio_EUR"].mean())
leading_product = df.loc[df["Ingresos_EUR"].idxmax(), "ID_Producto"]
revenue_share_top3 = float(df.nlargest(3, "Ingresos_EUR")["Ingresos_EUR"].sum() / total_revenue * 100) if total_revenue else 0.0
revenue_share_record = float(df.iloc[0]["Ingresos_EUR"] / total_revenue * 100) if total_revenue else 0.0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Unidades vendidas", f"{total_units:,}")
with kpi2:
    st.metric("Ingresos totales", f"€{total_revenue:,.2f}")
with kpi3:
    st.metric("Precio unitario medio", f"€{avg_unit_price:,.2f}")
with kpi4:
    st.metric("Producto líder", str(leading_product))

st.markdown("---")

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Top 3 productos</b><br>
            {revenue_share_top3:.1f}% del total de ingresos
        </div>
        """,
        unsafe_allow_html=True,
    )
with insight_col2:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Producto estrella</b><br>
            ID {leading_product} aporta {revenue_share_record:.1f}% del negocio
        </div>
        """,
        unsafe_allow_html=True,
    )
with insight_col3:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Promedio de precio</b><br>
            €{avg_unit_price:,.2f} por unidad
        </div>
        """,
        unsafe_allow_html=True,
    )

tab_overview, tab_products, tab_insights = st.tabs(["Overview", "Productos", "Insights"])

with tab_overview:
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        revenue_chart = px.bar(
            df,
            x="ID_Producto",
            y="Ingresos_EUR",
            title="Ingresos por producto",
            color="Ingresos_EUR",
            color_continuous_scale="Viridis",
        )
        revenue_chart.update_layout(
            xaxis_title="Producto",
            yaxis_title="Ingresos (€)",
            template="plotly_white",
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(revenue_chart, use_container_width=True)

    with chart_col2:
        share_chart = px.pie(
            df,
            names="ID_Producto",
            values="Ingresos_EUR",
            title="Participación de ingresos por producto",
            hole=0.4,
        )
        share_chart.update_traces(textinfo="percent+label")
        st.plotly_chart(share_chart, use_container_width=True)

    sales_col, price_col = st.columns(2)
    with sales_col:
        units_chart = px.bar(
            df,
            x="ID_Producto",
            y="Unidades_Vendidas",
            title="Unidades vendidas por producto",
            color="Unidades_Vendidas",
            color_continuous_scale="Blues",
        )
        units_chart.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(units_chart, use_container_width=True)

    with price_col:
        price_chart = px.scatter(
            df,
            x="Unidades_Vendidas",
            y="Ingresos_EUR",
            size="Ingresos_EUR",
            color="ID_Producto",
            hover_name="ID_Producto",
            title="Relación unidades vs ingresos",
        )
        price_chart.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(price_chart, use_container_width=True)

with tab_products:
    product_df = df[["ID_Producto", "Unidades_Vendidas", "Ingresos_EUR", "Precio_Unit_Promedio_EUR", "Cuota_Ingresos", "Cuota_Volumen"]].copy()
    display_df = product_df.copy()
    display_df["Cuota_Ingresos"] = display_df["Cuota_Ingresos"].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "0.0%")
    display_df["Cuota_Volumen"] = display_df["Cuota_Volumen"].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "0.0%")
    display_df["Ingresos_EUR"] = display_df["Ingresos_EUR"].map(lambda x: f"€{x:,.2f}")
    display_df["Precio_Unit_Promedio_EUR"] = display_df["Precio_Unit_Promedio_EUR"].map(lambda x: f"€{x:,.2f}")
    st.dataframe(display_df.sort_values("Unidades_Vendidas", ascending=False).reset_index(drop=True), use_container_width=True)

with tab_insights:
    top_products = df.nlargest(5, "Ingresos_EUR")
    top_products = top_products[["ID_Producto", "Ingresos_EUR", "Unidades_Vendidas"]].copy()
    top_products["Ingresos_EUR"] = top_products["Ingresos_EUR"].map(lambda x: f"€{x:,.2f}")

    st.subheader("Productos con mejor contribución")
    st.dataframe(top_products, use_container_width=True)

    st.subheader("Resumen ejecutivo")
    st.markdown(
        f"""
        - El producto con mayor contribución es el ID {leading_product}, representando aproximadamente {revenue_share_record:.1f}% del total de ingresos.
        - Los tres principales productos acumulan {revenue_share_top3:.1f}% de los ingresos totales, lo que sugiere una estructura concentrada del portafolio.
        - El precio promedio por unidad se sitúa en €{avg_unit_price:,.2f}, con un volumen total de {total_units:,} unidades comercializadas.
        """
    )

st.markdown("---")
st.caption("PlayLoop Analytics Portfolio • Diseño orientado a portfolio y presentación ejecutiva")
