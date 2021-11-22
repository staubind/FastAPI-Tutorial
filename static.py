from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", name="static"))
# "/static" refers to the sub-path the app is mounted inside of
# therefore, any path begining with /static will behandled here
# directory="static" refers to directory name that holds the static files
# name="static" refers to a name to be used by FastAPI


# this comes from starlette, so you could import that directly
# "mounting" means adding an independent application in a specific path that 
# takes care of handling sub-paths
# different than using apirouter because this is totally different app 
# not sure why though..?
# openapi docs won't include the mounted application api
