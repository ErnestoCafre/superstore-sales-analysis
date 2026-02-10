# Análisis de Ventas - Superstore (Proyecto End-to-End)


**Análisis exploratorio, limpieza de datos y dashboard interactivo de ventas de una cadena retail ficticia (EE.UU.).**  
Herramientas: Python (Pandas, Matplotlib/Seaborn), SQL, Power BI, Google Sheets.

## Objetivo del proyecto
Responder preguntas de negocio clave:  
- ¿Cómo evolucionaron las ventas y ganancias?  
- ¿Qué categorías/regiones generan más/menos profit?  
- ¿Impacto de los descuentos en las pérdidas?  
- Recomendaciones accionables para mejorar rentabilidad.

## Dataset
- **Fuente:** Kaggle - Superstore Dataset (Vivek468)  
- **Link:** [Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)  
- **Fecha de descarga:** Febrero 2026.

## Estructura del proyecto
```
├── data/
│   ├── raw/            # Datos originales inmutables
│   └── processed/      # Datos limpiados para modelado
├── notebooks/          # Jupyter notebooks (EDA)
├── sql/                # Scripts SQL (schema, queries)
├── src/                # Código Python (ETL)
├── docs/               # Documentación del proceso
│   └── process.md      # Proceso paso a paso detallado
├── .gitignore
├── requirements.txt
└── README.md
```

## Documentación del proceso
El detalle paso a paso del análisis se encuentra en [`docs/process.md`](docs/process.md).

## Setup
1. **Crear entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
2. **Ejecutar ETL:**
    ```bash
    python src/etl.py       # Limpia datos → data/processed/
    python src/load_db.py   # Carga en SQLite → data/superstore.db
    ```
