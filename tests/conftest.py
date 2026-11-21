import pytest

from website import create_app, db


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "test.sqlite3"
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
    })

    try:
        with app.app_context():
            db.create_all()
        yield app
    finally:
        with app.app_context():
            db.session.remove()
            db.engine.dispose()