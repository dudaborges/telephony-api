from fastapi import FastAPI
from tortoise import Tortoise
from database.config import TORTOISE_ORM
from database.register import register_tortoise


Tortoise.init_models(["src.database.models"], "models")


app = FastAPI()

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get('/')
def home():
    return 'test'
