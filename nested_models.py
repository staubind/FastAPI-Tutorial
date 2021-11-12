from typing import Optional, Set, List, Dict

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(...,gt=0, description="The pric emust be greater than zero") 
    # note that Field taken from pydantic, not fastapi
    # because we are doing validation on hte class's field, not on the data coming into the function
    # and actually, Query, Path are all instances Param which is a subclass of pydantic's FieldInfo, just like Field
    # and Body is also a subclass of FieldInfo
    tax: Optional[float] = None
    # if the tags have duplicate data when sent, they won't after passing through Pydantic's typing validation
    tags: Set[str] = set()
    images: Optional[List[Image]] = None
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": ["rock", "metal", "bar"],
#     "image": [
#       {
#         "url": "http://example.com/baz.jpg",
#         "name": "The Foo live"
#       }
#      ]
# }

# go ahead and nested models as deeply as you like
class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)): 
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images

# if you need to receive dicts - i.e. you don't know the keys you'll receive:
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights

# recall pydantic handles the data conversion for us
# so as long as the strings contain pure ints, they'll be converted and validated
