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
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "manufacturing_analytics"),
    }

    # Optional DB_PORT from environment variable
    if os.getenv("DB_PORT"):
        try:
            config["port"] = int(os.getenv("DB_PORT"))
        except ValueError:
            pass

    # Check Streamlit Cloud secrets if available
    try:
        import streamlit as st
        if hasattr(st, "secrets") and len(st.secrets) > 0:
            # 1. Section-based secrets: [mysql]
            if "mysql" in st.secrets:
                sec = st.secrets["mysql"]
                if "host" in sec: config["host"] = sec["host"]
                if "user" in sec: config["user"] = sec["user"]
                if "password" in sec: config["password"] = sec["password"]
                if "database" in sec: config["database"] = sec["database"]
                if "port" in sec: config["port"] = int(sec["port"])
                if "ssl_ca" in sec: config["ssl_ca"] = sec["ssl_ca"]

            # 2. Flat secrets (same shape as .env / .env.example)
            if "DB_HOST" in st.secrets: config["host"] = st.secrets["DB_HOST"]
            if "DB_USER" in st.secrets: config["user"] = st.secrets["DB_USER"]
            if "DB_PASSWORD" in st.secrets: config["password"] = st.secrets["DB_PASSWORD"]
            if "DB_NAME" in st.secrets: config["database"] = st.secrets["DB_NAME"]
            if "DB_PORT" in st.secrets: config["port"] = int(st.secrets["DB_PORT"])
            if "DB_SSL_CA" in st.secrets: config["ssl_ca"] = st.secrets["DB_SSL_CA"]
    except Exception:
        pass

    return config



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
