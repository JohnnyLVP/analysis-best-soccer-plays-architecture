from app import create_app
import pytest


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()

