from fastapi import FastAPI
from enum import Enum

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

@app.get('/items/{item_id}')
async def read_item(item_id: int):
    print(item_id, type(item_id))
    # note that 3 is automatically parsed as int rather than string
    # also provides error if you provide a float or non-coercable string
    return {"item_id": item_id}

# paths are evaluated in order, so make sure statics are before dynamic:
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

# if these weren't ordered properly, it would receive the string "me" as user_id
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# :path tells it that it should match any path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}