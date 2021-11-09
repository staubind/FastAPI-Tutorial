from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.get('/')
async def check_working():
    return {"Hello": "World"}

# uses Pydantic. May be worth looking into deeper: https://pydantic-docs.helpmanual.io/
