from fastapi import FastAPI, Form
from fastapi import FastAPI

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    # recall ... forces it to be required
    return {"username": username}
# one of the ways OAuth2 specifications can be used called "password flow"
# requires username and password be sent as form fields, not JSON.
# as an example of a time you would want to use this
# Form inherits directly from Body
# need to use Form direclty because otherwise the params will be interpreted as query params or body (JSON) params

# Forms apparently use different encoding than JSON - it uses "media type"
# called application/x-www-form-urlencoded
# but if it includes files it is encoded as: multipart/form-data

# You can declare multiple Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using application/x-www-form-urlencoded instead of application/json.

# This is not a limitation of FastAPI, it's part of the HTTP protocol.