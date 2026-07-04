from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from helpers.supabase.supabase_uploader import upload
from helpers.supabase.databasemain import add_transfer, get_row, generate_code
from fastapi import Form

app = FastAPI()

templates = Jinja2Templates(directory="frontend/html")
app.mount("/static", StaticFiles(directory="frontend/css"), name="static")


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
from fastapi.responses import JSONResponse

@app.post("/uploadfilebackend")
async def uploadfilebackend(
    request: Request,
    file: UploadFile = File(...)
):

    print("Route Started")

    code = generate_code()

    file_bytes = await file.read()



    upload(f"{code}_{file.filename}", file_bytes)

    add_transfer(code,"file",f"{code}_{file.filename}",f"{code}_{file.filename}")

    # TODO:
    # save_file(code, file.filename, storage_path)

    return JSONResponse({
        "success": True,
        "code": code
    })


@app.get("/generated")
def generated(request: Request, code: str):

    return templates.TemplateResponse(
        request=request,
        name="showgencode.html",
        context={
            "code": code
        }
    )

from fastapi.responses import FileResponse
from helpers.supabase.supabase_downloader import download_file

@app.post("/receivecode")
def receive_code(
    request: Request,
    code: str = Form(...)
):

    transfer = get_row(code.upper())

    if transfer is None:
        return templates.TemplateResponse(
            request=request,
            name="invalidcode.html",
            context={}
        )

    elif transfer["type"] == "file":

        local_file = download_file(
            transfer["storage_path"],
            transfer["filename"]
        )

        return FileResponse(
            path=local_file,
            filename=transfer["filename"],
            media_type="application/octet-stream"
        )

    elif transfer["type"] == "text":

        return templates.TemplateResponse(
            request=request,
            name="showtext.html",
            context={
                "code":code,
                "text": transfer["filename"]
            }
        )

    else:
        return templates.TemplateResponse(
            request=request,
            name="invalidcode.html",
            context={}
        )

    

@app.post("/clipboardsend")
def postcb(
    request: Request,
    text: str = Form(...)
):
    code = generate_code()

    add_transfer(code, "text", text, None)

    return templates.TemplateResponse(
        request=request,
        name="showgencode.html",
        context={
            "code": code
        }
    )