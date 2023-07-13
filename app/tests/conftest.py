import os
import pytest
from ..api import app as flask_app
from ..api import init


@pytest.fixture
def app():
    init()
    yield flask_app
    for file in os.listdir('.'):
        if file.endswith('.png'):
            os.remove(file)


@pytest.fixture
def client(app):
    return app.test_client()