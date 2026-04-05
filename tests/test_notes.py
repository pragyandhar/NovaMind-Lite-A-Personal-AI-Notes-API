from fastapi.testclient import TestClient
# ----------------------------------------
from app.main import app
# ----------------------------------------

client = TestClient(app)

def test_get_notes_returns_empty_list():
    # ACT
    response = client.get("/notes/")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == []

def test_create_note_returns_201():
    # ARRANGE
    payload = {"title": "Test Note", "content": "Hello World", "tags": []}
    # ACT
    response = client.post("/notes/create_note", json=payload)
    # ASSERT
    assert response.status_code == 201
    assert response.json()["title"] == "Test Note"

def test_get_nonexistent_note_returns_404():
    # ACT
    response = client.get("/notes/999999999")
    # ASSERT
    assert response.status_code == 404