import os
import tempfile
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# ======================================================
# Load .env for local development.
# On Streamlit Cloud this is a no-op (no .env file present) —
# secrets are injected directly as environment variables instead.
# ======================================================

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


def _get_setting(key, default=None):
    """Retrieve setting from environment variable or Streamlit secrets."""
    val = os.getenv(key)
    if val is not None and str(val).strip() != "":
        return val

    # Fallback to Streamlit secrets if running inside Streamlit Cloud
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets is not None:
            if key in st.secrets:
                return str(st.secrets[key])
            clean_key = key.lower().replace("db_", "")
            if "mysql" in st.secrets and clean_key in st.secrets["mysql"]:
                return str(st.secrets["mysql"][clean_key])
    except Exception:
        pass

    return default


def get_db_config():
    """Builds and returns the database configuration dictionary."""
    config = {
        "host": _get_setting("DB_HOST", "localhost"),
        "user": _get_setting("DB_USER", "root"),
        "password": _get_setting("DB_PASSWORD", ""),
        "database": _get_setting("DB_NAME", "manufacturing_analytics"),
        "port": int(_get_setting("DB_PORT", 3306)),
    }

    # ------------------------------------------------------
    # SSL support for hosted providers (e.g. Aiven)
    # Accepts either:
    # 1. DB_SSL_CA: A path to a downloaded ca.pem file
    # 2. DB_SSL_CA_CONTENT: The raw text of the CA certificate
    #    (ideal for Streamlit Cloud secrets to avoid local file dependency)
    # ------------------------------------------------------
    ssl_ca = _get_setting("DB_SSL_CA")
    ssl_ca_content = _get_setting("DB_SSL_CA_CONTENT")

    # If the certificate content was passed directly as text
    if ssl_ca_content or (ssl_ca and "-----BEGIN CERTIFICATE-----" in ssl_ca):
        raw_cert = ssl_ca_content if ssl_ca_content else ssl_ca
        temp_cert = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".pem")
        temp_cert.write(raw_cert)
        temp_cert.flush()
        temp_cert.close()
        ssl_ca = temp_cert.name

    if ssl_ca and os.path.exists(ssl_ca):
        config["ssl_ca"] = ssl_ca
        config["ssl_verify_cert"] = True

    return config


# Module-level DB_CONFIG for backward compatibility
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
