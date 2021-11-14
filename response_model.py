from typing import List, Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.networks import EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

@app.post("/items/", response_model=Item) # note that response_model is in the decorator
# used to:
    # convert output data to the type declaration
    # validate data
    # add json schema for the response
    # automatic documentation
async def create_item(item: Item):
    return item
    # The response model is declared in this parameter instead of as a function return type 
    # annotation, because the path function may not actually return that response model but 
    # rather return a dict, database object or some other model, and then use the 
    # response_model to perform the field limiting and serialization

    # not sure I totally understand the above snippet taken from the docs
    # I think what it's saying is that you can return a dict, for example,
    # and it will translate it into the correct class and return it appropriately
    # serialized

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db



# Don't do this in production!
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

# the syntax {"thing"} creates a set
# you can use a list or tuple, too, but fastapi will convert it to a set.
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=False, response_model_exclude={"tax"})
async def read_item(item_id: str):
    return items[item_id]

@app.get(
    "/items/{item_id}/name", 
    response_model=Item,
    response_model_include={"name", "description"}
)
async def read_item(item_id: str):
    return items[item_id]