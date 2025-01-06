import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.chat_service import ChatService
from services.vector_store import VectorStoreService
from config_prod import OPENAI_API_KEY

app = FastAPI()

# Enable CORS with environment-based origins
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
ALLOWED_ORIGINS = [
    FRONTEND_URL,
    'https://your-production-frontend.vercel.app'  # Add your Vercel domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class SearchQuery(BaseModel):
    query: str
    k: int = 3

class SearchResponse(BaseModel):
    results: list

chat_service = ChatService()
vector_store = VectorStoreService(OPENAI_API_KEY)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        response = await chat_service.get_chat_response(message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search", response_model=SearchResponse)
async def search_docs(query: SearchQuery):
    try:
        results = await vector_store.search(query.query, query.k)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 