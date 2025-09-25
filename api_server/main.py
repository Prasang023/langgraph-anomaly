import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api_server.controllers import ApiController
from fastapi.responses import StreamingResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

app = FastAPI(title="LangGraph API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to LangGraph API"}

class RunAgentRequest(BaseModel):
    query_id: str
    chat_type: str
    response_id: str = None
    agent_name_with_version: str = None

@app.post("/api/run-agent")
async def run_agent(request: RunAgentRequest):
    response = ApiController().run(
        query_id=request.query_id,
        chat_type=request.chat_type,
        response_id=request.response_id,
        agent_name_with_version=request.agent_name_with_version
    )
    return StreamingResponse(response, media_type="text/event-stream")

@app.post("/api/run-agent-simple")
async def run_agent_simple(request: RunAgentRequest):
    try:
        response = ApiController().run(
            query_id=request.query_id,
            chat_type=request.chat_type,
            response_id=request.response_id,
            agent_name_with_version=request.agent_name_with_version
        )
        
        # Collect all streaming response into a single string
        full_response = ""
        async for chunk in response:
            full_response += chunk
        
        return {
            "success": True,
            "response": full_response,
            "query_id": request.query_id,
            "agent_name": request.agent_name_with_version
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query_id": request.query_id
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
