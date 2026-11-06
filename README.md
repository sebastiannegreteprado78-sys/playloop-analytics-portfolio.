# PlayLoop Analytics Portfolio

Análisis de datos de una aplicación móvil de juegos centrado en adquisición de usuarios, actividad y monetización por compras dentro de la app (IAP). Este proyecto combina un notebook exploratorio con una base Python reutilizable y un dashboard para comunicar indicadores clave.

> Proyecto de portafolio con datos de ejemplo. Las métricas son descriptivas y no representan resultados reales de un producto en producción.

## Dashboard

[**Abrir dashboard interactivo**](https://datastudio.google.com/reporting/07e0f980-8727-4d53-baef-06ce66d33732)

![Captura del dashboard de PlayLoop](./Captura%20de%20pantalla%202026-11-03%20a%20la%28s%29%2015.18.21.png)

## Objetivos

- Explorar la actividad de usuarios y sesiones.
- Analizar ingresos y ventas de IAP sin reembolsos.
- Comparar usuarios por plataforma y país.
- Mantener una estructura reproducible para análisis y reportes.

## Estructura del repositorio

| Archivo o carpeta | Descripción |
| --- | --- |
| [`playloop.ipynb`](./playloop.ipynb) | Notebook original con el dashboard interactivo y exploración de datos. |
| [`main.py`](./main.py) | Script reutilizable para cargar datos y generar un resumen ejecutivo. |
| [`src/playloop_analysis.py`](./src/playloop_analysis.py) | Lógica central de limpieza, validación y cálculo de KPIs. |
| [`tests/test_playloop_analysis.py`](./tests/test_playloop_analysis.py) | Pruebas para confirmar la lógica clave del análisis. |
| [`requirements.txt`](./requirements.txt) | Dependencias mínimas para ejecutar el proyecto localmente. |
| [`PlayLoop_Analytics_Report - Reporte_Ejecutivo.csv`](./PlayLoop_Analytics_Report%20-%20Reporte_Ejecutivo.csv) | Resumen ejecutivo por producto y ventas. |

## Qué muestra el proyecto

- Usuarios únicos y volumen de sesiones registradas.
- Ingresos por compras IAP válidas, excluyendo reembolsos.
- Duración promedio por sesión.
- Distribución de usuarios por plataforma y principales países.
- Ventas y rentabilidad por producto.

## Cómo ejecutar

### 1) Preparar el entorno

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Ejecutar el análisis

```bash
python main.py --folder "/ruta/a/playloop_datasets"
```

La carpeta de entrada debe contener archivos como:
`compras.csv`, `gasto_ua.csv`, `ingresos_ads.csv`, `partidas.csv`, `productos_iap.csv`, `usuarios.csv` y `sesiones.csv`.

### 3) Revisar resultados

El script genera un resumen en CSV en `output/summary.csv` y además imprime un JSON con los indicadores principales.

## Mejora aplicada

La principal mejora fue separar la lógica de negocio del notebook para hacer el proyecto más mantenible:

- limpieza y validación de datos centralizada,
- cálculo de KPIs reutilizable,
- pruebas automatizadas para la lógica crítica,
- ejecución más simple fuera de Google Colab.

## Dashboard local profesional

Se ha añadido una interfaz ejecutable localmente con Streamlit para presentar el proyecto de forma más clara, visual y adecuada para portfolio.

### Ejecutar la app

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La app mostrará un resumen ejecutivo de productos, métricas clave y gráficos interactivos.

### 1) Branding premium

- Diseñamos una identidad visual más cuidada con colores sobrios y tarjetas de KPI.
- Se mejora la presentación para una demo profesional y entrevista técnica.

### 2) Métricas extra

- Se añadieron indicadores de contribución por producto.
- Se muestran insights clave para comunicar mejor la historia de negocio.
- La estructura facilita comparar volumen, ingresos y rendimiento por producto.

### 3) Preparación para despliegue

- La app está lista para ejecutarse con Streamlit.
- También se incluye un archivo Docker para despliegue en servicios cloud o entornos profesionales.
- Se puede publicar en servicios como Streamlit Cloud, Render o Railway.

### Despliegue con Docker

```bash
docker build -t playloop-analytics .
docker run -p 8501:8501 playloop-analytics
```

---

Desarrollado como proyecto de portafolio de analítica de datos.
