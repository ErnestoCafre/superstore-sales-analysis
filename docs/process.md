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
    - Cantidad de órdenes únicas sobre order id: 5009

- Total aproximado: Ventas $2,297,200.86 Profit $286,679.34 (calculado rápido en Excel).


## 2. Limpieza y transformación de datos (ETL)
- Script: [src/etl.py](../src/etl.py)
- Entrada: [data/raw/Sample - Superstore.csv](../data/raw/Sample%20-%20Superstore.csv) (encoding Windows-1252)
- Salida: [data/processed/superstore_clean.csv](../data/processed/superstore_clean.csv)
- Transformaciones realizadas:
    1. Estandarización de nombres de columnas a snake_case.
    2. Conversión de Order Date y Ship Date a formato datetime (de MM/DD/YYYY).
    3. Detección y eliminación de duplicados: 0 encontrados.
    4. Manejo de valores nulos: 0 valores nulos encontrados en el dataset.
    5. Conversión de `postal_code` a tipo texto (los códigos postales no son valores numéricos).
    6. Campo calculado: profit_margin = profit / sales (con protección contra división por cero).
    7. Campos de time intelligence: order_year, order_month, order_quarter.
- Resultado: 9,994 filas × 25 columnas (4 columnas nuevas agregadas).

## 3. Carga a Base de Datos
- Script: [src/load_db.py](../src/load_db.py)
- Entrada: [data/processed/superstore_clean.csv](../data/processed/superstore_clean.csv), [sql/schema.sql](../sql/schema.sql)
- Salida: Base de datos SQLite [data/superstore.db](../data/superstore.db)
- Proceso:
    1. Conexión a base de datos SQLite.
    2. Ejecución de schema SQL (creación de tabla `orders` y vistas).
    3. Limpieza de tabla `orders` (DELETE) para evitar duplicados.
    4. Carga de datos desde CSV procesado.
- Verificación: 9,994 filas insertadas en tabla `orders`.

### Decisiones técnicas

#### ¿Por qué SQLite y no solo CSV?
Para este proyecto, decidí implementar una base de datos SQLite intermedia (`data/superstore.db`) en lugar de conectar Power BI directamente al CSV por las siguientes razones de arquitectura de datos:

1.  **Integridad de Datos (Type Safety)**:
    - El CSV no fuerza tipos de datos. Una columna de fechas podría contener texto corrupto.
    - SQLite, a través de `sql/schema.sql`, define tipos explícitos (`REAL` para ventas, `DATE` para fechas). Si bien SQLite es flexible, esta capa actúa como un contrato de calidad.

2.  **Centralización de la Lógica (Business Logic in Views)**:
    - He creado vistas SQL (`v_sales_by_month`, `v_top_products`) en `sql/schema.sql`.
    - Esto permite que la lógica de negocio (ej. "cómo se define el top de productos") viva en el código SQL y no dispersa en fórmulas de Power BI o Excel.

3.  **Performance (Indexación)**:
    - Aunque con ~10k filas no es crítico, SQL permite indexar columnas (ej. `Order Date`) para consultas instantáneas, algo imposible en archivos planos (CSV) que requieren lectura secuencial completa.

#### ¿Por qué tabla plana (desnormalizada)?
El dataset se carga en una única tabla `orders` en lugar de normalizarlo en tablas separadas (customers, products, locations). Esto se justifica por:
- **Simplicidad**: El foco del proyecto es el análisis, no el modelado relacional.
- **Dataset pequeño**: Con ~10k filas, no hay beneficio de performance en normalizar.
- **Compatibilidad con Power BI**: Un modelo de tabla única simplifica la conexión y las medidas DAX.

#### Rol de los archivos
- **`sql/schema.sql` (Blueprint)**: Es el código fuente de la infraestructura. Define la estructura de las tablas y las vistas. Permite reproducir la base de datos desde cero si se borra el archivo `.db`.
- **`data/superstore.db` (Storage)**: Es el archivo binario donde residen los datos. Power BI o cualquier herramienta de análisis se conecta aquí para leer los datos ya limpios y estructurados.

## 4. Análisis Exploratorio de Datos (EDA)
- Notebook: [notebooks/01_eda.ipynb](../notebooks/01_eda.ipynb)
- Generado programáticamente con `nbformat` para reproducibilidad.
- Entrada: [data/processed/superstore_clean.csv](../data/processed/superstore_clean.csv)

### Secciones del análisis

1. **Carga y Validación de Datos**
    - Revalidación defensiva del dataset procesado (nulls, duplicados, totales de control).
    - Verificación de cardinalidad: 5,009 órdenes únicas, 793 clientes, 1,862 productos.
    - Totales de control: Ventas $2,297,200.86 — Profit $286,397.02.

2. **Evolución Temporal**
    - Ventas y profit por año, tendencia mensual, estacionalidad.
    - Análisis de divergencia ventas-profit: se identificó el *product mix effect* (ej. 2015: ventas -2.8% pero profit +24.4% por mejora en márgenes de Technology).
    - Estacionalidad: noviembre y diciembre concentran los picos de ventas.

3. **Rentabilidad por Categoría y Región**
    - Barras horizontales de profit por sub-categoría (verde/rojo).
    - Heatmaps: profit absoluto y margen por región × categoría.
    - Análisis por segmento de cliente (Consumer, Corporate, Home Office).

4. **Impacto de Descuentos**
    - Tabla cuantitativa de métricas por rango de descuento.
    - Gráfico de punto de quiebre: identificación del umbral donde el profit promedio se vuelve negativo.

5. **Top/Bottom Productos**
    - 10 productos más y menos rentables (drill-down a nivel micro).

6. **Conclusiones y Recomendaciones**
    - Plantilla de hallazgos estructurada: Hallazgo → Evidencia → Recomendación.

### Decisiones técnicas del EDA

- Se omitió el scatter plot de descuento vs profit por complejidad visual excesiva; se mantuvo solo la tabla y el gráfico de punto de quiebre por claridad.
- Se agregó análisis de product mix effect (margen por categoría por año) para explicar divergencias entre ventas y profit.
- El notebook se genera con un script Python (`create_eda_notebook.py`) para permitir modificaciones programáticas sin editar JSON manualmente.
