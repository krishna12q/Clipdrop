from upload_test import upload
from helpers.postgres.create_table import validate_code, save_file
from app import generate_code



code = generate_code()
filename = "dhingatika"

upload(filename)

save_file(code,filename,f"/bucket/{filename}")


validate_code(code)