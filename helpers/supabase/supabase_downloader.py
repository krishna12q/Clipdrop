from pathlib import Path
from helpers.supabase.supabase_client import supabase

def download_file(path: str, filename: str):

    file_bytes = supabase.storage.from_("uploads").download(path)

    with open(filename, "wb") as f:
        f.write(file_bytes)

    return filename