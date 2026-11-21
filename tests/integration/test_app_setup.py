def test_home_page_shows_only_flash_sale_products(app, seeded_products):
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert seeded_products["phone"]["product_name"] in html
    assert seeded_products["watch"]["product_name"] not in html