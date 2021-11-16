from typing import Optional
from fastapi import Depends, FastAPI
import fastapi

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    # second CommonQueryParams is the one that actually is called
    # the first CommonQueryParams is just for typing for editor support
    # however, FastApi allows you to do the following to help DRY it up:
    # commons: CommonQueryParams = Depends() is the same as the above
    response = {}
    if commons.q:
        response.update({"q": q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

