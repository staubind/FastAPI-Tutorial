from typing import Optional

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from pydantic.env_settings import SettingsSourceCallable

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000), # path param
    q: Optional[str] = None, # query param
    item: Optional[Item] = None # query param
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
# expects an object like:
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }


# Multiple body params:
# before: path operations would expect a json body w/ attributes of an Item 
class User(BaseModel):
    username: str
    fullname: Optional[str] = None

# in this case it will interpret both 
@app.put("/items/{item_id}")
# singular parameters are defaulted to Query, so if you want a singular value in the body, use Body
async def update_item(item_id: int, item: Item, user: User, importance: int = Body(...)): 
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
# expects an object like:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }

#multiple
@app.put("/items/{item_id}")
# singular parameters are defaulted to Query, so if you want a singular value in the body, use Body
async def update_item(
    *,
    item_id: int, 
    item: Item, 
    user: User, 
    importance: int = Body(..., gt=0), # also allows for metadata and validation
    q: Optional[str] = None): 
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q", q})
    return results
# expects an object like:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }



# Embed a single body parameter
# if using only a pydantic model with a singular parameter,
# then FastAPI will expect its body directly
# if you want it couched in JSON w/ a key,
# item: Item = Body(..., embed=True)

# for example:
class SingleItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: SingleItem = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
# in this case FastAPI expects:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }
# instead of:
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }
# note that one is couched in an item, where the other expects a flat object

