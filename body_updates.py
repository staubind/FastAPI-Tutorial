# you can use jsonable_encoder to conver the input data to dstoarable json
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "price": 62, "description": "The bartenders", "tax": 20.2},
    "baz": {"name": "Baz", "price": 50.2, "description": None, "tax": 10.5, "tags": []},
}

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    print('item is initially: ', item)
    update_item_encoded = jsonable_encoder(item)
    print('then update_item_encoded is: ', update_item_encoded)
    items[item_id] = update_item_encoded
    return update_item_encoded

# you can also use HTTP Patch to partially update data
# meaning you can send only the data you want to update, leaving the rest intact

# using pydantic's exclude_unset parameter
# you can also use exclude_unset instead of using a Patch
# item.dict(exclude_unset=True)
# creates a dict w/ only the data actively set (i.e. leave out defaults)

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

# you can use put, too, but this is really the purpose of patch
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data) 
    # uses pydantic's update param, that's why we make it into a model
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item