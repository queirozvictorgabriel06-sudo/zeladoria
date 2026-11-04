import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_URL")

if db_url:
    conexao = psycopg2.connect(db_url)
else:
    conexao = psycopg2.connect( 
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    port=os.getenv("DB_PORT"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conexao.cursor()