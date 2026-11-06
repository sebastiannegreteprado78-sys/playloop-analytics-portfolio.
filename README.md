# PlayLoop Analytics Portfolio

Data analysis for a mobile game application focused on user acquisition, activity, and monetization through in-app purchases (IAP). This project combines an exploratory notebook, a reusable Python data layer, and a dashboard to communicate key performance indicators.

> Portfolio project using sample data. Metrics are descriptive only and should not be interpreted as results from a real production product.

## Dashboard

[**Open interactive dashboard**](https://datastudio.google.com/reporting/07e0f980-8727-4d53-baef-06ce66d33732)

![PlayLoop dashboard screenshot](./Captura%20de%20pantalla%202026-11-03%20a%20la%28s%29%2015.18.21.png)

## Objectives

- Explore user and session activity.
- Analyze revenue and sales from IAP without refunds.
- Compare users by platform and country.
- Maintain a reproducible structure for analysis and reporting.

## Repository structure

| File or folder | Description |
| --- | --- |
| [`playloop.ipynb`](./playloop.ipynb) | Original notebook with the interactive dashboard and exploratory data analysis. |
| [`main.py`](./main.py) | Reusable script to load data and generate an executive summary. |
| [`src/playloop_analysis.py`](./src/playloop_analysis.py) | Core logic for cleaning, validation, and KPI calculation. |
| [`tests/test_playloop_analysis.py`](./tests/test_playloop_analysis.py) | Tests to validate the main analysis logic. |
| [`requirements.txt`](./requirements.txt) | Minimum dependencies to run the project locally. |
| [`PlayLoop_Analytics_Report - Reporte_Ejecutivo.csv`](./PlayLoop_Analytics_Report%20-%20Reporte_Ejecutivo.csv) | Executive summary by product and sales. |

## What the project shows

- Unique users and total sessions recorded.
- Revenue from valid IAP purchases, excluding refunds.
- Average session duration.
- User distribution by platform and top countries.
- Sales and profitability by product.

## How to run

### 1) Set up the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the analysis

```bash
python main.py --folder "/path/to/playloop_datasets"
```

The input folder should contain files such as:
`compras.csv`, `gasto_ua.csv`, `ingresos_ads.csv`, `partidas.csv`, `productos_iap.csv`, `usuarios.csv`, and `sesiones.csv`.

### 3) Review the results

The script generates a CSV summary in `output/summary.csv` and also prints a JSON with the main indicators.

## Improvement implemented

The main improvement was separating the business logic from the notebook to make the project more maintainable:

- centralized data cleaning and validation,
- reusable KPI calculation,
- automated tests for critical logic,
- simpler execution outside Google Colab.

## Professional local dashboard

A locally executable interface was added with Streamlit to present the project in a clearer, more visual, and portfolio-friendly way.

### Run the app

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app displays an executive summary of products, key metrics, and interactive charts.

### 1) Premium branding

- A cleaner visual identity was designed with refined colors and KPI cards.
- The presentation is more suitable for professional demos and technical interviews.

### 2) Additional metrics

- Product contribution indicators were added.
- Key insights are shown to communicate the business story more effectively.
- The structure helps compare sales volume, revenue, and product performance.

### 3) Deployment readiness

- The app is ready to run with Streamlit.
- A Docker file is included for cloud deployment or professional environments.
- It can be published on services such as Streamlit Cloud, Render, or Railway.

### Docker deployment

```bash
docker build -t playloop-analytics .
docker run -p 8501:8501 playloop-analytics
```

---

Developed as a data analytics portfolio project.
