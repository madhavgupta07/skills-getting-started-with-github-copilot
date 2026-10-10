from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate-test@mergington.edu"

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    second = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "remove-test@mergington.edu"

    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
