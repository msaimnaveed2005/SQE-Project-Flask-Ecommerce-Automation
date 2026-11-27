from threading import Thread

import pytest
from selenium import webdriver
from werkzeug.serving import make_server


@pytest.fixture
def live_server(app):
    """Serve the isolated Flask app over HTTP for one browser test."""
    host = "127.0.0.1"
    with make_server(host, 0, app, threaded=True) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://{host}:{server.server_port}"
        finally:
            server.shutdown()
            thread.join()


@pytest.fixture
def browser():
    """Open a fresh Chrome session for one browser test."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()
