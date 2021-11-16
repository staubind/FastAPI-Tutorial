# you can add a list of dependencies to the path operator function 
# if you don't want there to be a returnable 
# if you have a returnable but put the dependency in the path decorator
# it will ignore the returnables

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

async def verify_token(x_token: str = Header(...)):
    if x_token == '':
        raise HTTPException(status_code=403, detail="You are not allowed.")
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key == '':
        raise HTTPException(status_code=403, detail="You are not allowed.")
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "foo"}, {"item": "Bar"}]