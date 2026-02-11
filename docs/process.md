# Proceso Paso a Paso

## 1. Descarga y comprensión inicial del dataset
- Descargado el CSV desde Kaggle.  
- Abierto en Google Sheets para vista rápida.  
- Observaciones:
    - Total de filas: 9.994
    - Total de columnas: 21
    - Datos de columnas: Row ID (Identificador único de la fila), Order ID (Identificador único de la orden), Order Date (Fecha de la orden), Ship Date (Fecha de envío), Ship Mode (Modo de envío), Customer ID (Identificador único del cliente), Customer Name (Nombre del cliente), Segment (Segmento del cliente), Country (País), City (Ciudad), State (Estado), Postal Code (Código postal), Region (Región), Product ID (Identificador único del producto), Category (Categoría del producto), Sub-Category (Subcategoría del producto), Product Name (Nombre del producto), Sales (Ventas), Quantity (Cantidad), Discount (Descuento), Profit (Ganancia).
    - Columnas con formato de fecha: Order Date, Ship Date.
    - Columnas con formato numérico: Sales, Quantity, Discount, Profit.
    - Columnas con formato de texto: Row ID, Order ID, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name.
    - 4 regiones (Central, East, South, West).
    - Profit puede ser negativo (pérdidas reales en algunas ventas).
    - Categorías principales: Technology, Furniture, Office Supplies.
    - Cantidad de órdenas únicas sobre order id: 5009

- Total aproximado: Ventas $2,297,200.86 Profit $286,679.34 (calculado rápido en Excel).


## 2. Limpieza y transformación de datos (ETL)
- Script: [src/etl.py](src/etl.py)
- Entrada: [data/raw/Sample - Superstore.csv](data/raw/Sample%20-%20Superstore.csv) (encoding Windows-1252)
- Salida: [data/processed/superstore_clean.csv](data/processed/superstore_clean.csv)
- Transformaciones realizadas:
    1. Estandarización de nombres de columnas a snake_case.
    2. Conversión de Order Date y Ship Date a formato datetime (de MM/DD/YYYY).
    3. Detección y eliminación de duplicados: 0 encontrados.
    4. Manejo de valores nulos: Postal Code (11 nulls en Burlington, VT) rellenados con '00000'.
    5. Campo calculado: profit_margin = profit / sales (con protección contra división por cero).
    6. Campos de time intelligence: order_year, order_month, order_quarter.
- Resultado: 9,994 filas × 24 columnas (3 columnas nuevas agregadas).