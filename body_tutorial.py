from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
# declares a JSON "object" that looks like:
# {
# "name": "Foo",
# "description": "An optional description",
# "price": 45.2,
# "tax": 3.5
# }
# this would also be valid, given two params are optional:
# {
# "name": "Foo",
# "price": 45.2,
# }

app = FastAPI()

# uses Pydantic. May be worth looking into deeper: https://pydantic-docs.helpmanual.io/
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# if param also in path, used as path param
# if param is singular type (int, float, str, bool) interpreted as query param
# if param is a Pydantic model, it will be taken as a request body

@app.get('/')
async def check_working():
    return {"Hello": "World"}

