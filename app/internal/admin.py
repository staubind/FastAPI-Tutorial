from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}

# say that you couldn't edit this file because other apps depend on it, then 
# import it and define your own custom router in main.py