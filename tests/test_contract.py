from fastapi.testclient import TestClient
from backend.app import app
c=TestClient(app)
def test_health_schema():
    x=c.get("/healthz")
    assert x.status_code==200 and x.json()["mode"]=="standalone"
def test_simulated_sms_explicit():
    x=c.post("/api/v1/sessions",json={"channel":"sms-sim"})
    assert x.status_code==200 and x.json()["simulation"] is True
def test_invalid_channel_rejected():
    assert c.post("/api/v1/sessions",json={"channel":"pstn"}).status_code==422
