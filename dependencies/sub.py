from typing import Optional
from fastapi import Cookie, Depends, FastAPI
import fastapi

app = FastAPI()

def query_extractor(q: Optional[str] = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q

@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    # if you have multiple dependencies that all have a dependency in common,
    # you can use use_cache=False to force it to calculate that common dependency
    # for each time it's called, otherwise FastAPI is smart enough to call it once
    return {"q_or_cookie": query_or_default}

