
import os
import mysql.connector
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )

        return connection

    except mysql.connector.Error as error:
        print(f"Database connection error: {error}")
        return None
