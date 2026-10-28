from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.sqlite_repo import SQLiteRepository
from app.infrastructure.chroma_repo import ChromaRepository
from app.infrastructure.gemini_service import GeminiService
from app.infrastructure.ollama_service import OllamaService
from app.infrastructure.lmstudio_service import LMStudioService 
from app.use_cases.ingest_property import IngestPropertyUseCase
from app.use_cases.query_advisor import QueryAdvisorUseCase
from app.use_cases.get_chat_history import GetChatHistoryUseCase
from app.use_cases.delete_chat_session import DeleteChatSessionUseCase
from app.delivery.api_v3 import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Clean Architecture Architecture Real Estate RAG")

# --- Configure CORS Security Layer ---
# Define explicit origin access lists. Avoid using ["*"] in production settings.
origins = [
    "http://localhost:3000",      # Standard React local dev address
    "http://localhost:5173",      # Standard Vite / Vue / Svelte local dev address
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows explicit cross-origin requests from these locations
    allow_credentials=True,           # Allows browser cookies or authentication credentials
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicit HTTP methods permitted
    allow_headers=["*"],              # Allows all custom operational header requests (Content-Type, Authorization, etc.)
)
# -------------------------------------


# 1. Instantiate Adapters (Infrastructure)
sqlite_repo = SQLiteRepository()
chroma_repo = ChromaRepository()
gemini_api = GeminiService()
ollama_local = OllamaService()
lmstudio_local = LMStudioService()

# 2. Inject Adapters into Application Use Cases
app.state.ingest_property_use_case = IngestPropertyUseCase(sqlite_repo, chroma_repo)
app.state.query_advisor_use_case = QueryAdvisorUseCase(sqlite_repo, chroma_repo, gemini_api, ollama_local, lmstudio_local)
app.state.get_chat_history_use_case = GetChatHistoryUseCase(sqlite_repo)
app.state.delete_chat_session_use_case = DeleteChatSessionUseCase(sqlite_repo)

# 3. Mount Delivery Endpoints
app.include_router(router)
