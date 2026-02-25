import pandas as pd
import numpy as np
import pathlib

# Configuration - Robust Path Handling
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / 'data' / 'raw' / 'Sample - Superstore.csv'
PROCESSED_DATA_PATH = BASE_DIR / 'data' / 'processed' / 'superstore_clean.csv'

def load_data(filepath):
    """Load data from CSV file."""
    print(f"Loading data from {filepath}...")
    try:
        # Try reading with default encoding, fallback to latin1 or cp1252 if needed
        df = pd.read_csv(filepath, encoding='windows-1252')
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_data(df):
    """Perform data cleaning and transformation."""
    if df is None:
        return None
    
    print("Cleaning data...")
    
    # 1. Standardize column names (lowercase, snake_case)
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # 2. Convert dates
    date_cols = ['order_date', 'ship_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce') # Assuming US format based on previous view
    
    # 3. Handle duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"Removing {duplicates} duplicate rows.")
        df = df.drop_duplicates()

    # 4. Handle nulls
    nulls = df.isnull().sum()
    null_cols = nulls[nulls > 0]
    if len(null_cols) > 0:
        print(f"Null values found:\n{null_cols}")
    else:
        print("No null values found.")
    
    # 4.1 Convert postal_code to string with zero-padding (US zip codes = 5 digits)
    if 'postal_code' in df.columns:
        df['postal_code'] = df['postal_code'].astype(int).astype(str).str.zfill(5)
        
    # 5. Calculated fields
    if 'sales' in df.columns and 'profit' in df.columns:
        df['profit_margin'] = np.where(df['sales'] != 0, df['profit'] / df['sales'], 0.0)   # Avoid division by zero
    
    # 6. Extract time intelligence columns
    if 'order_date' in df.columns:
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_quarter'] = df['order_date'].dt.quarter
    
    print(f"Data cleaned. New shape: {df.shape}")
    return df

def save_data(df, filepath):
    """Save processed data to CSV."""
    if df is None:
        return
    
    print(f"Saving processed data to {filepath}...")
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print("Data saved successfully.")

def main():
    df = load_data(RAW_DATA_PATH)
    df_clean = clean_data(df)
    save_data(df_clean, PROCESSED_DATA_PATH)
    
    # Simple profile
    print("\nData Profile:")
    print("-" * 20)
    print(df_clean.info())
    print("\nMissing Values:")
    print(df_clean.isnull().sum()[df_clean.isnull().sum() > 0])

if __name__ == "__main__":
    main()
