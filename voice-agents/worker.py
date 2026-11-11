"""LiveKit hosted/locally connected worker. Requires provisioned LiveKit Inference."""
import os
import httpx
from livekit.agents import Agent,AgentSession,JobContext,WorkerOptions,cli,function_tool,RunContext

API=os.getenv("LSK_API_URL","http://127.0.0.1:18743")
class CustomerAgent(Agent):
    def __init__(self,session_id:str):
        self.sid=session_id
        super().__init__(instructions=(
            "You are an LSK fictional food ingredient distributor support agent. "
            "Do not reveal customer or order details until customer has verified using the secure browser form. "
            "Never request PIN aloud. For order information, use tools; never invent status or dates. "
            "Offer human transfer for uncertainty, disputes, invoices, sensitive or unsupported requests. "
            "Confirm before any sensitive action. Do not claim the human is connected merely because a case was created."))
    async def _call(self,method,path,**kwargs):
        async with httpx.AsyncClient(timeout=5) as client:
            r=await client.request(method,API+path,**kwargs)
            if r.status_code==403: return {"error":"verification_required","instruction":"Ask customer to verify via secure browser form"}
            if r.status_code>=400: return {"error":"service_unavailable","instruction":"Apologize and offer human support"}
            return r.json()
    @function_tool()
    async def lookup_orders(self,context:RunContext)->str:
        """List orders for a browser-verified customer; no unverified account access."""
        return str(await self._call("GET",f"/api/v1/sessions/{self.sid}/orders"))
    @function_tool()
    async def lookup_delivery(self,context:RunContext,order_id:str)->str:
        """Read delivery status only for an order owned by the verified customer."""
        return str(await self._call("GET",f"/api/v1/sessions/{self.sid}/orders/{order_id}/delivery"))
    @function_tool()
    async def transfer_to_human(self,context:RunContext,reason:str)->str:
        """Create a case in the human queue with consent-allowed context."""
        return str(await self._call("POST",f"/api/v1/sessions/{self.sid}/transfer",json={"reason":reason[:500]}))
async def entrypoint(ctx:JobContext):
    room=ctx.room.name
    if not room.startswith("lsk-"): return
    sid=room[4:]
    await ctx.connect()
    # Model identifiers resolved by LiveKit Inference. No scripted/model-free substitute.
    session=AgentSession(stt=os.getenv("LSK_VOICE_STT","deepgram/nova-3"),
                         llm=os.getenv("LSK_VOICE_LLM","openai/gpt-4.1-mini"),
                         tts=os.getenv("LSK_VOICE_TTS","cartesia/sonic-3"))
    await session.start(room=ctx.room,agent=CustomerAgent(sid))
    await session.generate_reply(instructions="Welcome the customer and explain secure browser verification is needed for private order information.")
if __name__=="__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
