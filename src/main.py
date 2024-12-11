import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient
from uvicorn.main import logger

from src.routes.api import router as template_router

load_dotenv()

mongo_uri = os.environ.get('ME_CONFIG_MONGODB_URL')
db_name = os.environ.get('DB_NAME')


def app() -> FastAPI:
    app = FastAPI()
    app.include_router(template_router, tags=["templates"], prefix="")
    app.mongodb_client = MongoClient(mongo_uri)
    app.database = app.mongodb_client.get_database(db_name)

    return app
