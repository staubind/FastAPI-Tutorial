from typing import Optional, List

from fastapi import FastAPI, Header
import fastapi

app = FastAPI()

@app.get("/items/")
async def read_item(user_agent: Optional[str] = Header(None, convert_underscores=False)):
    # most standard headers are separate by the following char: -
    # obviously, not python friendly, so Header converts from
    # _ to - to extract headers
    # Headers are also case insensitive
    # convert_underscores=False prevents the autoconversion talked about above
    # note that some servers and proxies will not allow underscores.
    return {"User-Agent": user_agent}

@app.get("/itemss/")
async def read_tokens(x_token: Optional[List[str]] = Header(None)):
    # most standard headers are separate by the following char: -
    # obviously, not python friendly, so Header converts from
    # _ to - to extract headers
    # Headers are also case insensitive
    # convert_underscores=False prevents the autoconversion talked about above
    # note that some servers and proxies will not allow underscores.
    return {"X-Token values": x_token}