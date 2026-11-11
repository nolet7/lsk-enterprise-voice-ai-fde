"""Explicitly simulated SMS inbound adapter (not a telephony provider)."""
import httpx
async def send_simulated_inbound(api_url,operator_key,session_id,text):
    async with httpx.AsyncClient() as c:
        r=await c.post(api_url+"/api/v1/events",
            headers={"X-Operator-Key":operator_key},
            json={"session_id":session_id,"event":"sms_simulated","payload":{"length":len(text)}})
        r.raise_for_status()
        return {"simulated":True,"accepted":r.json()["accepted"]}
