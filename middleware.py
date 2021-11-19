import time

from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time) # proprietary headers can be created via 'X-...'
    # not totally sure what call_next is here - do we have to pass a specific path operation function?
    # when does this run wrt dependencies? before, after, during...?
    return response