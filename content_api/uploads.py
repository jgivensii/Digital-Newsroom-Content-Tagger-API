from content_api.responses import ApiError
from werkzeug.datastructures import FileStorage

def read_upload(file_storage: FileStorage | None, allowed_extension: set[str], max_bytes: int) -> tuple[bytes, str]:
    """ validates an uploaded file and return its bytes """
   
    if file_storage is None or not file_storage.filename:
        raise ApiError("validation_failed", 422, "no file uploaded - mulit-part/form-data expected")
    
    extension = file_storage.filename.rsplit(".", 1)[-1].lower()
    if extension not in allowed_extension:
        raise ApiError("Unsupported Media Type", 415, f"{extension} is not supported. Expected one of teh following: {[e for e in allowed_extension]}")
    
    
    content = file_storage.read()
    
    if len(content)> max_bytes:
        raise ApiError("File size too large", 413, f"file is {len(content)} bytes; max allowed is {max_bytes} bytes.")
    
    if not content:
        raise ApiError("validation_failed", 422, "uploaded file is empty")
    
    return content, file_storage.filename

