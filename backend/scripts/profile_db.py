import psycopg2
import os
from dotenv_vault import load_dotenv

load_dotenv()

# Fetch variables
USER = os.getenv("SUPABASE_DB_USER")
PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
HOST = os.getenv("SUPABASE_DB_HOST")
PORT = os.getenv("SUPABASE_DB_PORT")
DBNAME = os.getenv("SUPABASE_DB_NAME")


try:
    connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME,
            sslmode='require'
        )
    print("Connection successful!")

    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()

    # with open("sql/profiles.sql", "r") as f:
    with open("sql/profiles.sql", "r", encoding="utf-8") as f:
        for cmd in f.read().split(";"):
            # if cmd.strip():
            cursor.execute(cmd)

    connection.commit()
    cursor.close()
    connection.close()
    print("Connection closed.")

    print("Database initialized successfully")

except Exception as e:
    print(f"Failed to connect: {e}")
