import pytest

from website import create_app, db
from website.models import Customer, Product
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


@pytest.fixture
def seeded_products(app):
    products = {
        "phone": {
            "product_name": "SQE Test Phone",
            "current_price": 1000.0,
            "previous_price": 1200.0,
            "in_stock": 10,
            "product_picture": "/static/images/phone.jpg",
            "flash_sale": True,
        },
        "watch": {
            "product_name": "SQE Test Watch",
            "current_price": 500.0,
            "previous_price": 600.0,
            "in_stock": 10,
            "product_picture": "/static/images/oraimoWatch.jpg",
            "flash_sale": False,
        },
    }

    with app.app_context():
        db.session.add_all(Product(**product) for product in products.values())
        db.session.commit()

    return products


@pytest.fixture
def seeded_customer(app):
    credentials = {
        "email": "shopper@example.test",
        "password": "sqe-test-password",
    }

    with app.app_context():
        customer = Customer(
            id=2,
            email=credentials["email"],
            username="SQE Shopper",
        )
        customer.password = credentials["password"]
        db.session.add(customer)
        db.session.commit()

    return credentials