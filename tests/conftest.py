import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.breakfast import Breakfast

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_breakfasts(app):
    breakfast1 = Breakfast(name="Congee", rating=8, prep_time=10)
    breakfast2 = Breakfast(name="Waffle", rating=7, prep_time=3)

    db.session.add(breakfast1)
    db.session.add(breakfast2)
    db.session.commit()