from website.models import Customer

def test_home_page_shows_only_flash_sale_products(app, seeded_products):
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert seeded_products["phone"]["product_name"] in html
    assert seeded_products["watch"]["product_name"] not in html

def test_seeded_customer_has_working_credentials(app, seeded_customer):
    with app.app_context():
        customer = Customer.query.filter_by(email=seeded_customer["email"]).one()

        assert customer.id != 1
        assert customer.verify_password(seeded_customer["password"])