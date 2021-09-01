from fastapi import FastAPI
from blog.routers.user_router import user_router
from blog.routers.post_router import post_router

app = FastAPI()


@app.get("/", tags=['Home'])
def hello_world():
    return {"Hello": "World"}


app.include_router(user_router)
app.include_router(post_router)
