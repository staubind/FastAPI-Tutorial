from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.post("/files/")
async def create_files(files: List[bytes] = File(...)): # File inherits from Form
    # bytes causes it to be taken in as bytes
    # return {"file_size": len(file)}
    return {"file_sizes": [len(file) for file in files]}
# whole file contents will be stored in memory - fine for small sizes

@app.post("/uploadfiles/") # upload spools the file - if it fills memory it slides to disk
async def create_upload_file(files: List[UploadFile] = File(...)): # files are uploaded as form data
    # UploadFiles have standard async await methods that a python file object has
    # When you use the async methods, FastAPI runs the file methods in a threadpool and awaits for them.
    # if inside of a non-async function,
    # you don't have to call await on teh reading methods

    return {"filename": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)