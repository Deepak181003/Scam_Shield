"""Small smoke test for the ScamShield backend."""
from app import app

client = app.test_client()

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_analyze():
    r = client.post("/api/analyze", json={
        "content": "Your bank account will be blocked today. Send the OTP immediately.",
        "input_type": "message",
    })
    assert r.status_code == 200
    data = r.get_json()
    assert data["success"] is True
    assert "risk" in data["result"]
    assert "scam_type" in data["result"]
    assert "stage" in data["result"]

def test_validation():
    r = client.post("/api/analyze", json={"content": ""})
    assert r.status_code == 400

def test_batch():
    r = client.post("/api/analyze/batch", json={
        "items": [
            {"content": "Send your OTP immediately.", "input_type": "message"},
            {"content": "The meeting is at 5 PM.", "input_type": "message"},
        ]
    })
    assert r.status_code == 200
    assert r.get_json()["count"] == 2

if __name__ == "__main__":
    test_health()
    test_analyze()
    test_validation()
    test_batch()
    print("All backend smoke tests passed.")
