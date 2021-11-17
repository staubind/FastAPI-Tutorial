from typing import Optional
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    disabled: Optional[bool] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", fullname="John Doe"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_items(current_user: User = Depends(get_current_user)):
    return {"user": current_user}