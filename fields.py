from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

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

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)): 
    results = {"item_id": item_id, "item": item}
    return results

