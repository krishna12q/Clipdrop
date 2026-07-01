from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import random
import string
import psycopg2
from fastapi.staticfiles import StaticFiles


app = FastAPI()

templates = Jinja2Templates(directory="frontend/html")
app.mount("/static", StaticFiles(directory="frontend/css"), name="static")

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="clipdrop",
    user="postgres",
    password="luminous in"
)

cursor = conn.cursor()





@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)


@app.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="fileupload.html",
    context={}
)

@app.get("/clipboard")
def upload_text(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="clipboard.html",
        context={}
    )

@app.get("/receive")
def receive_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="receive.html",
        context={}
    )

from fastapi import UploadFile, File

@app.post("/uploadfilebackend")
async def uploadfilebackend(file: UploadFile = File(...)):

    print(file.filename)

    return {
        "filename": file.filename
    }