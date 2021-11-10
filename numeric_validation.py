from typing import Optional
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get('/items/{item_id}')
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"), # ... makes it required - path params ALWAYS required
    # using path allows us, like with Query, to do additional validation and metadata on path parameters
    q: Optional[str] = Query(None, alias="item-query") # recall alias is what the var will be presented as in the url
):
    results = {"Item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# say you want to declare q required and nothing else for that param
# and you still need item_id
@app.get('/itemss/{item_id}')
async def read_items(
    q: str,
    item_id: int = Path(..., title="The ID of the item to get") # ... makes it required - path params ALWAYS required
    # using path allows us, like with Query, to do additional validation and metadata on path parameters
    # q: str python complains about it not having a default value and being after one w/ a default - move it to the start
):
    results = {"Item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# use * for kwargs
@app.get('/itemsss/{item_id}')
async def read_items(
    *, # using star here allows you to have the param defenitions out of order (note q has no default where item_id does)
    # what's happening here is that python is calling everything as a keyword arg, 
    # even those without a default val
    item_id: int = Path(..., title="The ID of the item to get"), # ... makes it required - path params ALWAYS required
    # using path allows us, like with Query, to do additional validation and metadata on path parameters
    q: str # recall alias is what the var will be presented as in the url
):
    results = {"Item_id": item_id}
    if q:
        results.update({"q": q})
    return results

######## VALIDATION #########

@app.get('/itemssss/{item_id}/{other_item_id}')
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=1), # ge here represents greater-or-equal-to
    other_item_id: int = Path(..., title="The id of the other item to get", gt=0, le=1000), # gt = greater than, le = less than or equal to
    q: Optional[str] = Query(None, alias="item-query"),
    size: float = Query(..., gt=0, lt=10.5)
):
    results = {"Item_id": item_id}
    if q:
        results.update({"q": q})
    return results