"""
Script to apply database/schema.sql to the target MySQL database (e.g. Aiven defaultdb).
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

from database.db_connection import get_connection

def run_schema():
    schema_path = Path(__file__).resolve().parent / "database" / "schema.sql"
    if not schema_path.exists():
        print(f"[ERROR] Schema file not found at {schema_path}")
        return

    with open(schema_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    print("[INFO] Connecting to database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("[SUCCESS] Connected successfully!")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return

    print("[INFO] Executing schema.sql statements...")
    # Split queries by semicolon, filtering out empty ones
    raw_statements = sql_content.split(";")
    for stmt in raw_statements:
        cleaned = stmt.strip()
        if cleaned:
            try:
                cursor.execute(cleaned)
            except Exception as err:
                print(f"[WARN] Statement failed: {err}\nQuery: {cleaned[:60]}...")

    conn.commit()

    # Verify tables
    cursor.execute("SHOW TABLES;")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\n[SUCCESS] Found {len(tables)} tables in database:")
    for t in sorted(tables):
        print(f"  - {t}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_schema()
