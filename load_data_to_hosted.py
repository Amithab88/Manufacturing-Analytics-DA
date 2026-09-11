"""
Script to import raw CSV datasets into the target MySQL database in proper foreign-key order.
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
from database.db_connection import get_connection

def clean_val(val):
    if pd.isna(val):
        return None
    return val

def import_csvs():
    raw_dir = Path(__file__).resolve().parent / "data" / "raw"
    if not raw_dir.exists():
        print(f"[ERROR] Data folder not found at {raw_dir}")
        return

    conn = get_connection()
    cursor = conn.cursor()

    load_plan = [
        ("Factories", raw_dir / "factories.csv"),
        ("Shifts", raw_dir / "shifts.csv"),
        ("Employees", raw_dir / "employees.csv"),
        ("Machines", raw_dir / "machines.csv"),
        ("Products", raw_dir / "products.csv"),
        ("Production_Batches", raw_dir / "production_batches.csv"),
    ]

    for table_name, csv_path in load_plan:
        if not csv_path.exists():
            print(f"[WARN] Skipping {table_name}: {csv_path.name} not found.")
            continue

        print(f"[INFO] Reading {csv_path.name} for table `{table_name}`...")
        df = pd.read_csv(csv_path)
        # Replace NaN with None
        df = df.replace({np.nan: None})

        cols = list(df.columns)
        placeholders = ", ".join(["%s"] * len(cols))
        col_names = ", ".join([f"`{c}`" for c in cols])
        insert_sql = f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders})"

        rows = [tuple(clean_val(x) for x in row) for row in df.itertuples(index=False, name=None)]

        batch_size = 1000
        total_rows = len(rows)
        print(f"[INFO] Inserting {total_rows:,} rows into `{table_name}`...")

        for i in range(0, total_rows, batch_size):
            chunk = rows[i:i + batch_size]
            cursor.executemany(insert_sql, chunk)
            conn.commit()

        print(f"[SUCCESS] Loaded {total_rows:,} rows into `{table_name}`.")

    cursor.close()
    conn.close()
    print("\n[ALL DONE] Finished importing CSV data into hosted database!")

if __name__ == "__main__":
    import_csvs()
