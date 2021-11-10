# uses Pydantic. May be worth looking into deeper: https://pydantic-docs.helpmanual.io/
from fastapi import FastAPI, Query
from typing import Optional, List
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

# we can even add regex for parameters
@app.get("/items/")
async def read_items(q: str = Query("fixedquery", min_length=3, max_length=50), regex="^fixedquery$"): # recall, using None implies it is optional Optional is purely for the editor
    # first param to Query sets default value, second sets constraint
    # also explicity defines it as a query param, rather than a path param
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# if you need to use Query and want it to be required (not have a default value)
@app.get("/item/")
async def read_items(q: str = Query(..., min_length=3, max_length=50), regex="^fixedquery$"): # recall, using None implies it is optional Optional is purely for the editor
    # using ... for first param makes it required
    # first param to Query sets default value, second sets constraint
    # also explicity defines it as a query param, rather than a path param
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/itemss/")
async def read_items(q: Optional[List[str]] = Query(None)):
    # note that you must use Query explicity with list otherwise it interprets it as the body of the request
    print(q)
    query_items = {"q": q}
    return query_items

@app.get("/items/")
async def read_items(q: list = Query([])):
    # in this case the contents of the list will not be observed
    query_items = {"q": q}
    return query_items


# DECLARING METADATA
@app.get("/idems/")
async def read_idems(
    q: Optional[str] = Query(None, 
        title = "Query string", 
        min_length=3,
        description = "Query string for the items to search in the database that have a good match.")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Using Aliases for variable names:
@app.get("/itemsss/")
async def read_itemsss(
    q: Optional[str] = Query(None, alias="item-query", deprecated=True,) # using deprecated=True allows it to show that it's being deprecated in future releases
    # this way q will be the actual variable name used for the query parameter "item-query"
):
    results = {"items": [{"item_id": "Bar"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

