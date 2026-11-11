"""Lightweight API concurrency smoke test; records real local durations."""
import asyncio,time,json,os
import httpx
URL=os.getenv("LSK_API_URL","http://127.0.0.1:18743")
N=int(os.getenv("LSK_LOAD_USERS","4"))
async def one(client,i):
    t=time.perf_counter()
    try:
        r=await client.post(URL+"/api/v1/sessions",json={"channel":"web-chat"})
        result={"status":r.status_code,"duration_ms":round((time.perf_counter()-t)*1000,1)}
        if r.status_code==200:
            await client.post(URL+"/api/v1/sessions/"+r.json()["session_id"]+"/end")
        return result
    except Exception as e:return {"error":type(e).__name__,"duration_ms":round((time.perf_counter()-t)*1000,1)}
async def main():
    async with httpx.AsyncClient(timeout=10) as client:
        items=await asyncio.gather(*(one(client,i) for i in range(N)))
    print(json.dumps({"test":"local_api_only_not_voice_calls","concurrency":N,"results":items},indent=2))
if __name__=="__main__":asyncio.run(main())
