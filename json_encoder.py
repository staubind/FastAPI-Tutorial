# jsonable_encoder() is used for turning different data types into 
# something json compatible
# used if you need to need to turn data into usable stuff for a db or something

from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    # converts the model to a dict and datetime to a str
    # result of calling it is something that can be encoded w/
    # standard json.dumps()
    # it does NOT return a large str containing the data in JSON format
    # (i.e. as a string)
    # it's a python standard data structure w/ values and sub-values
    # that are compatible w/ json