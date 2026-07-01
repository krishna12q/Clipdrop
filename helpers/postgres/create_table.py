import os
import psycopg2
from dotenv import load_dotenv
import string
import random

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
CREATE TABLE IF NOT EXISTS transfers(
    id SERIAL PRIMARY KEY,
    code VARCHAR(5) UNIQUE NOT NULL,
    type VARCHAR(10) NOT NULL,
    filename TEXT,
    storage_path TEXT,
    text_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

connection.commit()


def save_file(code, filename, storage_path):

    cursor.execute("""
    INSERT INTO transfers
    (code, type, filename, storage_path)
    VALUES (%s, %s, %s, %s)
    """, (
        code,
        "file",
        filename,
        storage_path
    ))

    connection.commit()

def validate_code(code: str):

    cursor.execute("""
        SELECT *
        FROM transfers
        WHERE code = %s
    """, (code,))

    result = cursor.fetchone()

    print(result)


def generate_code(length=5):

    chars = string.ascii_uppercase + string.digits

    while True:

        code = "".join(random.choice(chars) for _ in range(length))

        if not validate_code(code):
            return code
        
def get_row_from_code(code:str):
    cursor.execute("""
    SELECT * FROM transfers WHERE code = %s 
    """,(code,))

    resultrow = cursor.fetchone()

    return resultrow