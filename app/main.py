from fastapi import FastAPI
from routers.root import root_router

app = FastAPI()


@app.get("/", tags=['Home'])
def hello_world():
    return {"Hello": "World"}


app.include_router(root_router)
