from fastapi import FastAPI
from models import user_model
from database import engine
from routers import user_router


app = FastAPI()

user_model.Base.metadata.create_all(engine)


@app.get("/", tags=['Home'])
def hello_world():
    return {"Hello": "World"}


app.include_router(user_router.router)
