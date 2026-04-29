import pytest
from fastapi.testclient import TestClient
import copy
import src.app as app_module

# Initial activities data for resetting between tests
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Train and play soccer matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in plays and learn theater skills",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["mason@mergington.edu", "charlotte@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["harper@mergington.edu", "logan@mergington.edu"]
    }
}

@pytest.fixture
def client():
    # Reset the activities to initial state for each test
    app_module.activities = copy.deepcopy(initial_activities)
    return TestClient(app_module.app, follow_redirects=False)

def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success(client):
    response = client.post("/activities/Chess Club/signup?email=newstudent@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up newstudent@example.com for Chess Club" == data["message"]
    # Verify added to participants
    activities = client.get("/activities").json()
    assert "newstudent@example.com" in activities["Chess Club"]["participants"]

def test_signup_duplicate(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up" == data["detail"]

def test_signup_unknown_activity(client):
    response = client.post("/activities/Unknown Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" == data["detail"]

def test_unregister_success(client):
    response = client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered michael@mergington.edu from Chess Club" == data["message"]
    # Verify removed from participants
    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

def test_unregister_not_signed_up(client):
    response = client.post("/activities/Chess Club/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not registered for this activity" == data["detail"]

def test_unregister_unknown_activity(client):
    response = client.post("/activities/Unknown Activity/unregister?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" == data["detail"]