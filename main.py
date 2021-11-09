from fastapi import FastAPI
from enum import Enum
from typing import Optional

# create an enum class
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
# this creates a set of validation values to check against

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get('/')
async def root():
    return {"message": "Hello World"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# params not part of path params are query params
# going to: http://127.0.0.1:8000/items/?skip=1&limit=1
# will return [{"item_name": "Bar"}]
# query params initially string, but using typing converts them and validates them
@app.get("/items/")
async def read_item(skip: int=0, limit: int=10):
    return fake_items_db[skip : skip + limit]

# can set optional parameters by setting their default val to None w/ Optional[type]
@app.get('/items/{item_id}')
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    print(item_id, type(item_id))
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    # note that 3 is automatically parsed as int rather than string
    # also provides error if you provide a float or non-coercable string
    return item

# if you don't provide default value and go to http://127.0.0.1:8000/item/foo-item you'll get an error in the json
# but if you use http://127.0.0.1:8000/item/foo-item?needy=sooooneedy it comes through
@app.get('/item/{item_id}') # used /item -> singular to keep all endpoints available in this tutorial
async def read_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

@app.get('/ite/{item_id}')
async def read_item(
    item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# paths are evaluated in order, so make sure statics are before dynamic:
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

# if these weren't ordered properly, it would receive the string "me" as user_id
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# you can also use multiple parameters and multiple query params in the same endpoint
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# :path tells it that it should match any path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}





