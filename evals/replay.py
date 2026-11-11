"""Deterministic API-level replay; not a substitute for real speech eval."""
import json,sys
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app import app
def run():
    c=TestClient(app)
    results=[]
    for line in (Path(__file__).parent/"scenarios.jsonl").read_text().splitlines():
        if not line.strip(): continue
        row=json.loads(line)
        sid=c.post("/api/v1/sessions",json={"channel":"web-chat"}).json()["session_id"]
        if row.get("verified"):
            auth=c.post(f"/api/v1/sessions/{sid}/verify",json={"customer_id":row["customer_id"],"code":"2468"})
            assert auth.status_code==200
        expected=row["expected"]
        if expected=="withhold_private_data":
            res=c.get(f"/api/v1/sessions/{sid}/orders")
            passed=res.status_code==403
        elif expected=="lookup_order_delivery":
            res=c.get(f"/api/v1/sessions/{sid}/orders/O-1001/delivery")
            passed=res.status_code==200 and res.json()["status"]=="shipped"
        elif expected in ("deny_cross_customer","unknown_or_escalate"):
            order="O-2001" if expected=="deny_cross_customer" else "O-9999"
            res=c.get(f"/api/v1/sessions/{sid}/orders/{order}/delivery")
            passed=res.status_code==404
        elif expected=="human_escalation":
            res=c.post(f"/api/v1/sessions/{sid}/transfer",json={"reason":"Invoice dispute"})
            passed=res.status_code==200
        else:
            # No speech model inference in this deterministic API replay.
            results.append({"scenario":row["id"],"status":"not_tested_model"})
            continue
        results.append({"scenario":row["id"],"status":"pass" if passed else "fail"})
    print(json.dumps(results,indent=2))
    return int(any(x["status"]=="fail" for x in results))
if __name__=="__main__":sys.exit(run())
