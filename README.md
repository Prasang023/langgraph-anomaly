A FastAPI-based server that provides LangGraph agent execution capabilities with streaming responses.

## Installation

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

### Using uvicorn directly
```bash
uvicorn api_server.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on:
- **Local**: http://localhost:8000
- **Network**: http://0.0.0.0:8000

## API Endpoints

### 1. Run Agent (Streaming Response)
```http
POST http://localhost:8000/api/run-agent
Content-Type: application/json

{
  "query_id": "unique_query_id",
  "chat_type": "user_query",
  "response_id": "optional_response_id",
  "agent_name_with_version": "open_loop_agent_v1"
}
```

**Response:** Server-Sent Events (SSE) stream

### 3. Run Agent (Simple Response)
```http
POST http://localhost:8000/api/run-agent-simple
Content-Type: application/json

{
  "query_id": "unique_query_id",
  "chat_type": "user_query",
  "response_id": "optional_response_id",
  "agent_name_with_version": "open_loop_agent_v1"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Agent response content",
  "query_id": "unique_query_id",
  "agent_name": "open_loop_agent_v1"
}
```

### Call any api twice and observe the initial states and other values logged carefully, and then answer the questions please.
