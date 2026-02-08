# Superstore Data Analysis Project

## Overview
Comprehensive data analysis project for a global retail chain ("Superstore"). This project demonstrates the full data lifecycle:
1.  **Business Understanding**: Defining KPIs and hypotheses.
2.  **Data Engineering (ETL)**: Cleaning and modeling data using Python and SQL.
3.  **Analysis**: Exploratory Data Analysis (EDA) and SQL querying.
4.  **Visualization**: Interactive Power BI dashboard.

## Structure
- `data/`: Contains raw and processed datasets.
    - `raw/`: Original immutable data.
    - `processed/`: Cleaned data ready for modeling.
- `notebooks/`: Jupyter notebooks for EDA and prototyping.
- `sql/`: SQL scripts for schema creation and analysis.
- `src/`: Python source code for reproducible ETL scripts.
- `docs/`: Project documentation.

## Setup
1.  **Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  **Data**:
    - Raw data is located in `data/raw/Sample - Superstore.csv`.

## Tools
- **Python**: Pandas, Matplotlib, Seaborn.
- **SQL**: SQLite (embedded) or PostgreSQL.
- **Power BI**: Dashboarding.
