from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED) # these just hold hte values, but helps you find em
# note that this is just a default. will learn in the advanced version how to send a non-default code
# can also use an int, like 201
# can also receive IntEnum like Python's http.HTTPStatus
async def create_item(name: str):
    return {"name": name}