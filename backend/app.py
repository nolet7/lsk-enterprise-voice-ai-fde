"""Standalone legacy-first contact-center simulator, with guarded LiveKit bridge."""
import os, time, uuid, hmac
from collections import deque
from threading import RLock
from typing import Literal
from fastapi import FastAPI, HTTPException, Header, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="LSK Contact Center", version="1.0")
LOCK = RLock()
TENANT = os.getenv("LSK_DEMO_TENANT", "tenant-demo")
OPERATOR_KEY = os.getenv("LSK_OPERATOR_KEY", "change-this-local-operator-key")
# Demo fixtures intentionally non-real; no account data from real customers.
CUSTOMERS = {"C100":{"name":"Demo Foods LLC","pin":"2468","tenant":TENANT},
             "C200":{"name":"Harbor Ingredients Ltd","pin":"1357","tenant":TENANT}}
ORDERS = {"O-1001":{"customer_id":"C100","items":["Vanilla extract"],"status":"shipped","eta":"2026-11-14","tracking":"DEMO-471"},
          "O-2001":{"customer_id":"C200","items":["Cocoa powder"],"status":"processing","eta":"2026-11-17","tracking":None}}
CALLS = {}
CASES = {}
EVENTS = deque(maxlen=1000)
METRICS = {"tool_ok":0,"tool_fail":0,"transfers":0,"calls":0}
ACTIVE_LIMIT = int(os.getenv("LSK_MAX_ACTIVE_CALLS", "5"))
CAPTURE = os.getenv("LSK_CAPTURE_TRANSCRIPTS", "false").lower() == "true"
class Start(BaseModel):
    channel: Literal["web-voice","web-chat","sms-sim"] = "web-voice"
    consent_transcript: bool = False
class Verify(BaseModel):
    customer_id: str
    code: str
class Message(BaseModel):
    text: str = Field(min_length=1,max_length=2000)
class Case(BaseModel):
    reason: str = Field(min_length=1,max_length=500)
class Inbound(BaseModel):
    session_id: str
    event: str = Field(min_length=1,max_length=100)
    payload: dict = Field(default_factory=dict)
def get_call(sid):
    c = CALLS.get(sid)
    if not c or c["tenant"] != TENANT:
        raise HTTPException(404,"Unknown session")
    return c
def verified(sid):
    c=get_call(sid)
    if not c["verified"]:
        raise HTTPException(403,"Customer verification required")
    return c
def operator(key):
    if not hmac.compare_digest(key or "", OPERATOR_KEY):
        raise HTTPException(401,"Operator key required")
def event(sid, kind, data=None):
    EVENTS.append({"at":time.time(),"session":sid,"type":kind,"data":data or {}})
@app.get("/healthz")
def health():
    return {"ok":True,"mode":"standalone","tenant":TENANT}
@app.get("/")
def root():
    from pathlib import Path
    return HTMLResponse((Path(__file__).parents[1]/"frontend"/"index.html").read_text())
@app.post("/api/v1/sessions")
def start(data:Start):
    with LOCK:
        active=sum(c["state"] not in ("ended","transferred") for c in CALLS.values())
        if active >= ACTIVE_LIMIT:
            raise HTTPException(429,"Call capacity reached; please try later")
        sid=uuid.uuid4().hex
        CALLS[sid]={"id":sid,"tenant":TENANT,"channel":data.channel,"verified":False,"customer_id":None,
                    "consent":data.consent_transcript,"state":"queued","history":[],"started":time.time(),"queue":"general"}
        METRICS["calls"]+=1
        event(sid,"inbound",{"channel":data.channel})
        return {"session_id":sid,"state":"queued","simulation":data.channel=="sms-sim"}
@app.post("/api/v1/sessions/{sid}/verify")
def verify(sid:str, data:Verify):
    with LOCK:
        c=get_call(sid)
        if c["state"] in ("ended","transferred"):
            raise HTTPException(409,"Session closed")
        if c.get("failed_verifications",0)>=3:
            raise HTTPException(429,"Verification locked; transfer to human")
        person=CUSTOMERS.get(data.customer_id)
        if not person or person["tenant"]!=TENANT or not hmac.compare_digest(data.code,person["pin"]):
            c["failed_verifications"]=c.get("failed_verifications",0)+1
            event(sid,"verify_failed")
            raise HTTPException(403,"Verification failed")
        c.update(verified=True,customer_id=data.customer_id,state="active")
        event(sid,"verified")
        return {"verified":True,"customer_id":data.customer_id}
@app.get("/api/v1/sessions/{sid}/orders")
def orders(sid:str):
    with LOCK:
        c=verified(sid)
        METRICS["tool_ok"]+=1
        event(sid,"orders_lookup")
        return {"orders":[{"id":key,"status":value["status"]} for key,value in ORDERS.items() if value["customer_id"]==c["customer_id"]]}
@app.get("/api/v1/sessions/{sid}/orders/{oid}/delivery")
def delivery(sid:str,oid:str):
    with LOCK:
        c=verified(sid)
        rec=ORDERS.get(oid)
        if not rec or rec["customer_id"]!=c["customer_id"]:
            METRICS["tool_fail"]+=1
            raise HTTPException(404,"Order not found for verified customer")
        METRICS["tool_ok"]+=1
        event(sid,"delivery_lookup",{"order_id":oid})
        return {"order_id":oid,"status":rec["status"],"eta":rec["eta"],"tracking":rec["tracking"]}
@app.post("/api/v1/sessions/{sid}/messages")
def message(sid:str,data:Message):
    with LOCK:
        c=get_call(sid)
        if c["state"] in ("ended","transferred"):
            raise HTTPException(409,"Session closed")
        # Never send personal/account detail in unverified chat.
        response="Please verify in the secure form before discussing orders, or ask to speak to a human."
        if c["verified"]:
            response="I can help with order status, delivery, product questions, or transfer you to an agent."
        if c["consent"] and CAPTURE:
            c["history"].append({"role":"customer","text":data.text})
            c["history"].append({"role":"system","text":response})
        event(sid,"chat",{"length":len(data.text)})
        return {"reply":response,"simulated":True}
@app.post("/api/v1/sessions/{sid}/transfer")
def transfer(sid:str,data:Case):
    with LOCK:
        c=get_call(sid)
        if c["state"]=="ended":
            raise HTTPException(409,"Session ended")
        caseid="CASE-"+uuid.uuid4().hex[:8]
        CASES[caseid]={"id":caseid,"session":sid,"tenant":TENANT,"reason":data.reason,
                       "customer_id":c["customer_id"] if c["verified"] else None,
                       "verified":c["verified"],"queue":"general","state":"waiting",
                       "context":list(c["history"]) if c["consent"] and CAPTURE else []}
        c["state"]="transferred"
        METRICS["transfers"]+=1
        event(sid,"human_transfer",{"case_id":caseid})
        return {"case_id":caseid,"queue":"general","state":"waiting","handoff":"case_created_not_live_audio_bridge"}
@app.post("/api/v1/events")
def ingest(data:Inbound,x_operator_key:str=Header(default="")):
    operator(x_operator_key)
    get_call(data.session_id)
    event(data.session_id,data.event,{"adapter":"simulated"})
    return {"accepted":True,"simulated":True}
@app.get("/api/v1/operator/dashboard")
def dashboard(x_operator_key:str=Header(default="")):
    operator(x_operator_key)
    with LOCK:
        return {"queues":{"general":sum(x["state"]=="waiting" for x in CASES.values())},
                "cases":list(CASES.values()),"calls":[{k:v for k,v in c.items() if k not in ("history",)} for c in CALLS.values()],
                "recent_events":list(EVENTS)[-40:],"counters":dict(METRICS)}
@app.post("/api/v1/operator/cases/{caseid}/accept")
def accept(caseid:str,x_operator_key:str=Header(default="")):
    operator(x_operator_key)
    with LOCK:
        c=CASES.get(caseid)
        if not c: raise HTTPException(404,"Case not found")
        if c["state"]!="waiting": raise HTTPException(409,"Case not waiting")
        c["state"]="accepted"
        event(c["session"],"agent_accepted",{"case_id":caseid})
        return {"state":"accepted","case_id":caseid,"note":"Audio transfer requires telephony or LiveKit room coordination"}
@app.post("/api/v1/sessions/{sid}/end")
def end(sid:str):
    with LOCK:
        c=get_call(sid); c["state"]="ended"
        event(sid,"ended")
        return {"state":"ended"}
@app.post("/api/v1/sessions/{sid}/livekit-token")
def token(sid:str):
    with LOCK:
        c=get_call(sid)
        if c["channel"]!="web-voice" or c["state"] in ("ended","transferred"):
            raise HTTPException(409,"Voice not available for session")
    if os.getenv("LSK_ENABLE_VOICE","false").lower()!="true":
        raise HTTPException(503,"Live voice disabled; configure .env and worker")
    url=os.getenv("LIVEKIT_URL")
    key=os.getenv("LIVEKIT_API_KEY")
    secret=os.getenv("LIVEKIT_API_SECRET")
    if not all((url,key,secret)): raise HTTPException(503,"LiveKit credentials not configured")
    from livekit import api
    grant=api.VideoGrants(room_join=True,room="lsk-"+sid,can_publish=True,can_subscribe=True)
    jwt=api.AccessToken(key,secret).with_identity("customer-"+uuid.uuid4().hex).with_grants(grant).to_jwt()
    return {"url":url,"token":jwt,"room":"lsk-"+sid,"mode":"real_webrtc","expires_notice":"Use token immediately; rotate credentials as needed"}
@app.get("/metrics")
def metrics():
    from prometheus_client import generate_latest,CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
