from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo wrestlers"}

@app.get("/items/{item_id}")
async def read_items(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found") # raising an exceptoin sends the code
        # status and other relevant information
    return {"item": items[item_id]}

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}