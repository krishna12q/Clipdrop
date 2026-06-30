import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transfers (
    id SERIAL PRIMARY KEY,
    code VARCHAR(5) UNIQUE NOT NULL,
    type VARCHAR(10) NOT NULL,
    filename TEXT,
    storage_path TEXT,
    text_content
    )
""")

print("Connected to PostgreSQL!")