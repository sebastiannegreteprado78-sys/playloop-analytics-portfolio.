# PlayLoop Analytics Portfolio

Análisis de datos de una aplicación móvil de juegos: adquisición de usuarios, actividad y monetización mediante compras dentro de la app (IAP). El proyecto combina un notebook en Python con un dashboard interactivo y un reporte ejecutivo por producto.

> Proyecto de portafolio con datos de muestra. Las métricas son descriptivas y no deben interpretarse como resultados de un producto real.

## Dashboard

[**Abrir dashboard interactivo**](https://datastudio.google.com/reporting/07e0f980-8727-4d53-baef-06ce66d33732)

![Captura del dashboard de PlayLoop](./Captura%20de%20pantalla%202026-11-03%20a%20la%28s%29%2015.18.21.png)

## Objetivos

- Explorar el comportamiento y la actividad de los usuarios.
- Analizar ingresos y ventas de compras dentro de la aplicación.
- Comparar usuarios por plataforma y país.
- Presentar indicadores y tendencias en un dashboard fácil de consultar.

## Contenido del repositorio

| Archivo | Descripción |
| --- | --- |
| [`playloop.ipynb`](./playloop.ipynb) | Notebook de preparación y análisis de datos; genera el dashboard interactivo en Google Colab. |
| [`PlayLoop_Analytics_Report - Reporte_Ejecutivo.csv`](./PlayLoop_Analytics_Report%20-%20Reporte_Ejecutivo.csv) | Resumen ejecutivo de unidades vendidas e ingresos por producto IAP. |
| `Captura de pantalla…png` | Imagen de referencia del dashboard. |

## Qué muestra el dashboard

- Usuarios únicos y sesiones registradas.
- Ingresos por compras IAP válidas (excluye reembolsos) y duración promedio de sesión.
- Tendencia diaria de sesiones e ingresos.
- Distribución de usuarios por plataforma y principales países.
- Ventas e ingresos desglosados por producto.

## Herramientas

- **Python** y **pandas** para cargar, limpiar y agregar los datos.
- **Google Colab** para ejecutar el notebook.
- **HTML, JavaScript y Chart.js** para las visualizaciones interactivas.
- **CSV** para el reporte ejecutivo.

## Cómo ejecutar el notebook

1. Abre [`playloop.ipynb`](./playloop.ipynb) en Google Colab.
2. Sube los archivos de datos a Google Drive, dentro de la carpeta `playloop_datasets (1)`, o actualiza `folder_path` en el notebook para usar la ruta que prefieras.
3. Asegúrate de que la carpeta contenga estos archivos: `compras.csv`, `gasto_ua.csv`, `ingresos_ads.csv`, `partidas.csv`, `productos_iap.csv`, `usuarios.csv` y `sesiones.csv`.
4. Ejecuta las celdas en orden y autoriza el acceso a Drive cuando Colab lo solicite.

El notebook crea el dashboard dentro de la salida de Colab. Necesita conexión a internet para cargar Chart.js desde su CDN. Los archivos con datos fuente no están incluidos en este repositorio; no publiques datos personales o sensibles.

## Métricas y criterios

- Los ingresos principales del dashboard se calculan a partir de compras no reembolsadas.
- La actividad se resume a partir de los eventos de sesión registrados.
- El reporte CSV presenta ventas e ingresos por producto; revisa la moneda y el formato de importes al reutilizarlo con otros datos.

## Próximos pasos

- Documentar definiciones de métricas y supuestos de negocio.
- Incorporar análisis de retención y cohortes.
- Comparar el retorno de inversión de adquisición con los ingresos generados.
- Añadir pruebas de calidad y validaciones para los datos de entrada.

---

Desarrollado como proyecto de portafolio de analítica de datos.
