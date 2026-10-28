import os
import uuid
import traceback
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.infrastructure.sqlite_repo import SQLiteRepository
from app.infrastructure.chroma_repo import ChromaRepository
from app.infrastructure.gemini_service import GeminiService
from app.infrastructure.ollama_service import OllamaService
from app.infrastructure.lmstudio_service import LMStudioService 
from app.use_cases.ingest_property import IngestPropertyUseCase
from app.use_cases.query_advisor import QueryAdvisorUseCase
from app.use_cases.get_chat_history import GetChatHistoryUseCase
from app.use_cases.delete_chat_session import DeleteChatSessionUseCase
from app.domain.entities import ErrorLog
from app.delivery.api_v3 import router

load_dotenv()

# Set up clean async lifespan management context controls
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize db tables asynchronously on application starting phases
    await sqlite_repo.init_db()
    yield

app = FastAPI(title="Async High-Performance Advisor Engine", lifespan=lifespan)

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
# --- Global Exception Logging Middleware Interceptor ---
@app.middleware("http")
async def exception_logging_middleware(request: Request, call_next):
    try:
        # Pass the incoming connection onward to downstream targets
        response = await call_next(request)
        return response
    except Exception as exc:
        # 1. Capture system failure details
        error_id = str(uuid.uuid4())
        endpoint_path = request.url.path
        http_method = request.method
        error_msg = str(exc)
        trace_details = traceback.format_exc()

        # 2. Output detailed alert logs immediately to terminal console console
        print(f"\n [ERROR INTERCEPTED] | ID: {error_id}")
        print(f" Location: {http_method} {endpoint_path}")
        print(f" Message: {error_msg}\n")

        # 3. Persist diagnostic data using the registered database adapter
        try:
            sqlite_repo = request.app.state.sqlite_repository_instance
            error_entity = ErrorLog(
                log_id=error_id,
                endpoint=endpoint_path,
                method=http_method,
                error_message=error_msg,
                stack_trace=trace_details
            )
            sqlite_repo.save_error_log(error_entity)
        except Exception as db_err:
            print(f" Failed to commit error log to database registers: {str(db_err)}")

        # 4. Return clean, masked, uniform JSON error to clients
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected exception occurred within the advisory processing system.",
                "tracking_id": error_id
            }
        )


# 1. Instantiate Adapters (Infrastructure)
sqlite_repo = SQLiteRepository()
chroma_repo = ChromaRepository()
gemini_api = GeminiService()
ollama_local = OllamaService()
lmstudio_local = LMStudioService()

# Expose the repo instance on app state so middleware can access it directly
app.state.sqlite_repository_instance = sqlite_repo


# 2. Inject Adapters into Application Use Cases
app.state.ingest_property_use_case = IngestPropertyUseCase(sqlite_repo, chroma_repo)
app.state.query_advisor_use_case = QueryAdvisorUseCase(sqlite_repo, chroma_repo, gemini_api, ollama_local, lmstudio_local)
app.state.get_chat_history_use_case = GetChatHistoryUseCase(sqlite_repo)
app.state.delete_chat_session_use_case = DeleteChatSessionUseCase(sqlite_repo)

# 3. Mount Delivery Endpoints
app.include_router(router)
