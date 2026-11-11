import os
os.environ["LSK_OPERATOR_KEY"]="test-operator"
from fastapi.testclient import TestClient
import backend.app as app_module
from backend.app import app
client=TestClient(app)
def new(channel="web-chat"):
    r=client.post("/api/v1/sessions",json={"channel":channel})
    assert r.status_code==200
    return r.json()["session_id"]
def test_unauthenticated_order_is_denied():
    sid=new()
    assert client.get(f"/api/v1/sessions/{sid}/orders").status_code==403
def test_verified_order_and_cross_customer_protection():
    sid=new()
    assert client.post(f"/api/v1/sessions/{sid}/verify",json={"customer_id":"C100","code":"2468"}).status_code==200
    assert client.get(f"/api/v1/sessions/{sid}/orders").json()["orders"][0]["id"]=="O-1001"
    assert client.get(f"/api/v1/sessions/{sid}/orders/O-2001/delivery").status_code==404
def test_transfer_and_operator_access(monkeypatch):
    monkeypatch.setattr(app_module,"OPERATOR_KEY","test-operator")
    sid=new()
    c=client.post(f"/api/v1/sessions/{sid}/transfer",json={"reason":"Invoice question"})
    assert c.status_code==200
    assert c.json()["handoff"]=="case_created_not_live_audio_bridge"
    assert client.get("/api/v1/operator/dashboard").status_code==401
    assert client.get("/api/v1/operator/dashboard",headers={"X-Operator-Key":"test-operator"}).status_code==200
def test_verification_lock():
    sid=new()
    for _ in range(3):
        assert client.post(f"/api/v1/sessions/{sid}/verify",json={"customer_id":"C100","code":"bad"}).status_code==403
    assert client.post(f"/api/v1/sessions/{sid}/verify",json={"customer_id":"C100","code":"2468"}).status_code==429
def test_missing_live_voice_config_is_explicit():
    sid=new("web-voice")
    assert client.post(f"/api/v1/sessions/{sid}/livekit-token").status_code==503
