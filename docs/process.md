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
    - Cantidad de órdenas únicas sobre order id: 5035

- Total aproximado: Ventas $2,297,200.86 Profit $286,679.34 (calculado rápido en Excel).
