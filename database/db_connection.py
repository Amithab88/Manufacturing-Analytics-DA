import mysql.connector
from mysql.connector import Error

# ======================================================
# Database Configuration
# ======================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",      # Replace if your MySQL password is different
    "database": "manufacturing_analytics"
}

# ======================================================
# Create Database Connection
# ======================================================

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Database Connection Error: {e}")
        return None