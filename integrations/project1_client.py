"""Versioned optional Project 1 adapter. Fail closed; no silent contract assumptions."""
import os, httpx
class Project1Unavailable(Exception): pass
async def get_order(order_id:str,tenant:str,token:str):
    url=os.getenv("PROJECT1_API_URL")
    if not url: raise Project1Unavailable("Project 1 not configured; use standalone fixtures")
    async with httpx.AsyncClient(timeout=4) as client:
        r=await client.get(url.rstrip("/")+"/api/v1/orders/"+order_id,
                           headers={"Authorization":"Bearer "+token,"X-Tenant-ID":tenant})
        if r.status_code!=200: raise Project1Unavailable("Contract unavailable or rejected")
        data=r.json()
        if data.get("tenant_id")!=tenant: raise Project1Unavailable("Tenant mismatch")
        return data
