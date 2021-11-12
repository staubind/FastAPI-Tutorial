from typing import Optional
from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    # Cookie is a sister class of Path and Query. inherits from Param
    # to use it as a cookie you must declare it otherwise it assumes
    # it is a query param per usual.
    return {"ads_id": ads_id}