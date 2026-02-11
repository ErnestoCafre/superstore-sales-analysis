-- Schema for Superstore Data Analysis
-- Dialect: SQLite / PostgreSQL compatible

CREATE TABLE IF NOT EXISTS orders (
    row_id INTEGER PRIMARY KEY,
    order_id TEXT,
    order_date DATE,
    ship_date DATE,
    ship_mode TEXT,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL,
    profit_margin REAL,
    order_year INTEGER,
    order_month INTEGER,
    order_quarter INTEGER
);

-- View: Sales by Month
CREATE VIEW IF NOT EXISTS v_sales_by_month AS
SELECT 
    order_year, 
    order_month, 
    SUM(sales) as total_sales, 
    SUM(profit) as total_profit
FROM orders
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

-- View: Top Products by Profit
CREATE VIEW IF NOT EXISTS v_top_products AS
SELECT 
    product_name, 
    category, 
    SUM(sales) as total_sales, 
    SUM(profit) as total_profit
FROM orders
GROUP BY product_name, category
ORDER BY total_profit DESC
LIMIT 10;
