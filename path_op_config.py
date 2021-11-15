from typing import Optional, Set
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []

# all of the parameters in the decorator configure the documentation details
@app.post(
    "/items/", 
    response_model=Item, 
    status_code=status.HTTP_201_CREATED, 
    tags=["items"],
    summary="Create an item",
    response_description="The created item"
    # description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    # you can also create a description via markdown-irrigated docstrings
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]