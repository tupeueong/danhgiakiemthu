import os

import pytest

# Importing app creates the normal application object. During tests, point that
# import-time object at memory so it never opens the user's real vocabulary DB.
os.environ["LEXILOOP_DATABASE_URI"] = "sqlite:///:memory:"

from app import create_app
from models import db


@pytest.fixture()
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def add_formula(client):
    def _add_formula(content="E = mc²"):
        response = client.post("/api/formulas", json={"content": content})
        assert response.status_code == 201
        return response.get_json()["formula"]

    return _add_formula


@pytest.fixture()
def add_word(client):
    def _add_word(
        english="compelling",
        phonetic="/kəmˈpelɪŋ/",
        vietnamese="thuyết phục, hấp dẫn",
        part_of_speech="adjective",
        collocation="",
        word_pattern="",
        collocations=None,
        word_patterns=None,
        example="She made a compelling argument.",
        examples=None,
    ):
        payload = {
            "english": english,
            "phonetic": phonetic,
            "vietnamese": vietnamese,
            "part_of_speech": part_of_speech,
            "collocation": collocation,
            "word_pattern": word_pattern,
            "example": example,
        }
        if examples is not None:
            payload["examples"] = examples
        if collocations is not None:
            payload["collocations"] = collocations
        if word_patterns is not None:
            payload["word_patterns"] = word_patterns
        response = client.post(
            "/api/words",
            json=payload,
        )
        assert response.status_code == 201
        return response.get_json()["word"]

    return _add_word
