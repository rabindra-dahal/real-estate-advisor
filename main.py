from fastapi import FastAPI
from app.infrastructure.sqlite_repo import SQLiteRepository
from app.infrastructure.chroma_repo import ChromaRepository
from app.infrastructure.gemini_service import GeminiService
from app.infrastructure.ollama_service import OllamaService
from app.infrastructure.lmstudio_service import LMStudioService 
from app.use_cases.ingest_property import IngestPropertyUseCase
from app.use_cases.query_advisor import QueryAdvisorUseCase
from app.use_cases.get_chat_history import GetChatHistoryUseCase
from app.delivery.api_v3 import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Clean Architecture Architecture Real Estate RAG")

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

# 3. Mount Delivery Endpoints
app.include_router(router)
