import os
import sys
import copy
import pytest

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import app as _app_module
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    # Backup activities state and provide TestClient
    backup = copy.deepcopy(_app_module.activities)
    client = TestClient(_app_module.app)
    yield client
    # Restore activities to original state after each test
    _app_module.activities.clear()
    _app_module.activities.update(backup)
