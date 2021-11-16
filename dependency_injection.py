from typing import Optional
from fastapi import Depends, FastAPI

app = FastAPI()

# create a dependency or "dependable"
# A dependency is just a function that can take all the same params as a path operation func
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
# That's it.

# 2 lines.

# And it has the same shape and structure that all your path operation functions have.

# You can think of it as a path operation function without the "decorator" (without the @app.get("/some-path")).

# And it can return anything you want.

# In this case, this dependency expects:

# An optional query parameter q that is a str.
# An optional query parameter skip that is an int, and by default is 0.
# An optional query parameter limit that is an int, and by default is 100.
# And then it just returns a dict containing those values.

# Whenever a new request arrives, FastAPI will take care of:

# Calling your dependency ("dependable") function with the correct parameters.
# Get the result from your function.
# Assign that result to the parameter in your path operation function.




@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)): 
    # Depends only takes 1 argument
    # That function parameter, a function, takes arguments like a path function
    # more than functions can be used - to be learned later
    return commons

# I don't totally get it - so is it like middleware?
# or just like some pre-processing?
# I guess I'm confused about the use case.
# Why not just call the dependency on the first line of the path operation function?

# async or not:
# the usual.

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

#Other common terms for this same idea of "dependency injection" are:

# resources
# providers
# services
# injectables
# components