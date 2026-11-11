import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_URL")

def get_connection():
    if db_url:
        return psycopg2.connect(db_url)
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD")
    )

