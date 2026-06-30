from pathlib import Path
from Clipdrop.helpers.supabase.supabase_client import supabase

BASE_DIR = Path(__file__).parent

file_path = BASE_DIR / "test.txt"

with open(file_path, "rb") as f:
    response = supabase.storage.from_("uploads").upload(
        path="test.txt",
        file=f.read()
    )

print("Upload complete!")
print(response)