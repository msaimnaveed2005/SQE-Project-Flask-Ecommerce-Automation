from threading import Thread

import pytest
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
