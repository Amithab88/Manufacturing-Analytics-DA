import os
import mysql.connector
from mysql.connector import Error
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


# ======================================================
# Database Configuration
# Values are read from environment variables so credentials
# are never committed to source control. Set these in a local
# .env file (see .env.example) or your deployment environment.
# ======================================================

def get_db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "manufacturing_analytics"),
    }

DB_CONFIG = get_db_config()



def get_connection():
    """
    Returns a live MySQL connection, or raises a RuntimeError
    if the connection cannot be established.
    """
    try:
        connection = mysql.connector.connect(**get_db_config())

        if connection.is_connected():
            return connection

        raise RuntimeError("Database connection could not be established.")

    except Error as e:
        raise RuntimeError(f"Database Connection Error: {e}") from e
