from fastapi import FastAPI
from tortoise import Tortoise

from database.config import TORTOISE_ORM
from database.register import register_tortoise

Tortoise.init_models(['database.models'], 'models')
from routes import call_record

app = FastAPI()

app.include_router(call_record.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get('/')
async def home():
    return 'Hello, World!'
