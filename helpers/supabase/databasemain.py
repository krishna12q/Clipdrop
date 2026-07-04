from helpers.supabase.supabase_client import supabase
import random
import string

def add_transfer(code:str, filetype:str, filename:str, storage_path:str):
    supabase.table("transfers").insert(
        {
            "code": code, 
            "type": filetype,   
            "filename": filename,
            "storage_path": storage_path
        }
    ).execute()

def get_row(code: str):

    response = (
        supabase
        .table("transfers")
        .select("*")
        .eq("code", code)
        .single()
        .execute()
    )

    return response.data

def generate_code(length=5):

    chars = string.ascii_uppercase + string.digits

    while True:

        code = "".join(random.choice(chars) for _ in range(length))

        response = (
            supabase
            .table("transfers")
            .select("id")
            .eq("code", code)
            .execute()
        )

        if not response.data:
            return code