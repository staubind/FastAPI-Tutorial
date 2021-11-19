import time

from fastapi import FastAPI, Request
from fastapi.params import Depends

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    print('in middleware')
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time) # proprietary headers can be created via 'X-...'
    # not totally sure what call_next is here - do we have to pass a specific path operation function?
    # when does this run wrt dependencies? before, after, during...?
    return response

def some_dependency():
    print('in dependency')
    return 'hi'

@app.get('/')
async def some_func(response: str = Depends(some_dependency)):
    print('in func')
    return {"response": "hello world", "dependency": response}

@app.get('/hello')
async def some_func(response: str = Depends(some_dependency)):
    print('in func')
    return {"response": "hello", "dependency": response}