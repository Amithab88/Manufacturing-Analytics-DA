from database.db_connection import get_connection

connection = get_connection()

if connection:
    print("[SUCCESS] Database connection successful!")
    connection.close()
else:
    print("[ERROR] Database connection failed!")