import pandas as pd
import sqlite3
import pathlib

# Configuration - Robust Path Handling
# __file__ is the path to this script (src/load_db.py)
# .parent is 'src', .parent.parent is the project root
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / 'data' / 'processed' / 'superstore_clean.csv'
DB_PATH = BASE_DIR / 'data' / 'superstore.db'
SCHEMA_PATH = BASE_DIR / 'sql' / 'schema.sql'

def load_to_db():
    print(f"Loading from: {CSV_PATH}")
    if not CSV_PATH.exists():
        print(f"Error: Processed data not found at {CSV_PATH}. Run src/etl.py first.")
        return

    try:
        df = pd.read_csv(CSV_PATH, dtype={'postal_code': str})
        print(f"Read {len(df)} rows from CSV.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Connecting to database: {DB_PATH}")
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Apply Schema
        print(f"Applying schema from {SCHEMA_PATH}...")
        if not SCHEMA_PATH.exists():
             print(f"Error: Schema file not found at {SCHEMA_PATH}")
             conn.close()
             return

        with open(SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)
        
        # 2. Clean existing data (Idempotency)
        print("Cleaning existing data from 'orders' table...")
        cursor.execute("DELETE FROM orders;")
        
        # 3. Insert new data
        print("Inserting data...")
        # if_exists='append' acts as insert. We already cleaned the table.
        df.to_sql('orders', conn, if_exists='append', index=False)
        print(f"Success! Inserted {len(df)} rows into 'orders' table.")
        
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    load_to_db()
