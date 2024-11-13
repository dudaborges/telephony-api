from fastapi import FastAPI
from database.config import TORTOISE_ORM
from database.register import register_tortoise


app = FastAPI()

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get('/')
def home():
    return 'test'
