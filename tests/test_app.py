import os
import sys

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
import app as app_module


def test_get_activities(client: TestClient):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister(client: TestClient):
    email = "teststudent@mergington.edu"
    activity = "Chess Club"

    # Ensure participant not present
    assert email not in app_module.activities[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_del = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_del.status_code == 200
    assert email not in app_module.activities[activity]["participants"]

    # Unregistering again should return 404
    resp_del2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_del2.status_code == 404
