import pymysql

try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="my_portal"
    )
    print("Database exists and connection successful.")
    conn.close()
except pymysql.err.OperationalError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
