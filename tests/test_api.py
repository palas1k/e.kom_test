import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pymongo import MongoClient
from uvicorn.main import logger

from src.main import app
from tests.constants import TEMPLATES_TEST

load_dotenv()

app = app()
client = TestClient(app)

db_name = os.getenv("DB_NAME")


@pytest.fixture(scope="module")
def setup_database():
    app.mongodb_client = MongoClient('mongodb://localhost:27017/')
    app.database = app.mongodb_client.get_database(db_name)
    yield


def test_create_item(setup_database):
    for data in TEMPLATES_TEST:
        response = client.post("/set_data", json=data)
        assert response.status_code == 201


def test_get_item1(setup_database):
    data = {
        "name": "FormOrder",
        "user_email": "example@email.ru",
        "user_phone": "+7 911 111 11 11",
        "user_info": "text",
    }
    response = client.post("/get_form", json=data)
    assert response.status_code == 200
    assert response.json() == data.get('name')


def test_get_item2(setup_database):
    data = {
        "name": "FormAnswer",
        "user_email": "email",
        "user_phone": "+7 911 111 11 11",
        "user_answer": "string",
        "additional_info": "text"
    }

    response = client.post("/get_form", json=data)
    assert response.status_code == 200
    assert response.json() == data.get('name')


def test_get_non_located_item(setup_database):
    data = {
        "name1": "FormAnswer",
        "name2": "email",
        "user_phone": "+7 911 111 11 11",
    }

    response = client.post("/get_form", json=data)
    assert response.status_code == 200
    assert response.json() == {'name1': 'text', "name2": 'text', 'user_phone': 'phone'}
