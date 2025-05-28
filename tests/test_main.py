# test_main.py

import hashlib
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "form" in response.text  # Basic check if the form exists in HTML

def test_shorten_url():
    original_url = "https://www.example.com"
    short_hash = hashlib.md5(original_url.encode()).hexdigest()[:6]

    # Send form data (not JSON)
    response = client.post("/", data={"original": original_url})
    assert response.status_code == 200

    # Since response is HTML, check if the short URL appears somewhere in the page
    assert f"/{short_hash}" in response.text
