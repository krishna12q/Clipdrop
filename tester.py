from upload_test import upload
from helpers.postgres.create_table import validate_code, save_file, generate_code, get_row_from_code
from helpers.supabase.supabase_downloader import download_file



code = generate_code()
filename = f"{code}_dhingat67ika"

upload(filename)

save_file(code,filename,f"/{code}_{filename}")

get_row_from_code(code)

download_file(f"/{code}_{filename}")

validate_code(code)

