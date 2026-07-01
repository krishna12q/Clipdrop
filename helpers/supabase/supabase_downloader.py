from pathlib import Path
from supabase_client import supabase


def download_file(path:str,filename:str):
    file_bytes = supabase.storage.from_("uploads").download(path) 

    with open(filename, "wb") as f:
        f.write(file_bytes)

download_file("7Y833_dhingat67ika","dhingat67ika.txt")