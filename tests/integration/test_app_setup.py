def test_home_page_loads_with_test_database(app):
    response = app.test_client().get("/")
    assert response.status_code == 200