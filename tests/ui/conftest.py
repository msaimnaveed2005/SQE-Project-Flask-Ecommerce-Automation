import pytest

from tests.fixtures import ui


live_server = pytest.fixture(ui.live_server)
browser = pytest.fixture(ui.browser)
