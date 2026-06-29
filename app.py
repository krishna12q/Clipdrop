from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import random
import string
import psycopg2

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="clipdrop",
    user="postgres",
    password="luminous in"
)

cursor = conn.cursor()


def generate_code(length=5):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse(
        "fileupload.html",
        {"request": request}
    )


@app.get("/newcode")
def new_code():
    code = generate_code()

    return {
        "code": code
    }