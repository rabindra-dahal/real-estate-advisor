# 🏡 Resilient Real Estate Advisor (RAG + Clean Architecture)

An enterprise-grade Real Estate Advisory engine engineered using **Python**, **FastAPI**, and **Clean Architecture (Domain-Driven Design)** concepts. The platform combines semantic vector lookups with structural persistence layers, employing **Google Gemini** as the primary reasoning model and an automated offline fallback to a local **Ollama (Llama 3.1)** service.

---
### 🏗️ System Architecture

The application isolates core business domains from framework layers, drivers, and external API toolkits. 

---

### Core Architecture Layers
1. **Domain Layer (`app/domain`)**: Holds pure Python business structures (Entities) decoupled from third-party database attributes or web frameworks.
2. **Interfaces / Ports (`app/interfaces`)**: Abstract baseline contracts ensuring dependencies always point inward toward business logic.
3. **Use Cases (`app/use_cases`)**: Core processing workflows that coordinate data streams across vectors, relational stores, and LLM instances.
4. **Infrastructure Layer (`app/infrastructure`)**: Concrete plugin drivers housing active ChromaDB schemas, SQLite transaction tools, and Gemini connections.
5. **Delivery Layer (`app/delivery`)**: The presentation shell managing data translation validation (Pydantic DTOs) and network routing configurations.

---

## 📁 Repository Directory Blueprint

```text
real-estate-advisor/
├── app/
│   ├── domain/
│   │   └── entities.py           # Core Business Entities (Property, AdviceLog)
│   ├── use_cases/
│   │   ├── ingest_property.py    # Transaction workflows for property indexing
│   │   └── query_advisor.py      # Multi-model RAG context pipeline coordinator
│   ├── interfaces/
│   │   ├── relational_repo.py    # Relational repository interface blueprints
│   │   ├── vector_repo.py        # Semantic vector database interface blueprints
│   │   └── llm_service.py        # Language model generator structural blueprints
│   ├── infrastructure/
│   │   ├── sqlite_repo.py        # SQLAlchemy / SQLite physical implementation
│   │   ├── chroma_repo.py        # ChromaDB + SentenceTransformers integration
│   │   ├── gemini_service.py     # Gemini 3.5 Flash Lite engine handler
│   │   └── ollama_service.py     # Local Ollama fallback network connector
│   └── delivery/
│       ├── api_v3.py             # FastAPI routing and controller logic
│       └── dtos.py               # Pydantic schema validation structures
├── main.py                       # App initialization and dependency injection
├── seed_data.py                  # Simulation data populator script
├── check_logs.py                 # SQLite monitoring and auditing script
├── requirements.txt              # Project dependency tracking manifest
└── .env                          # Local credentials storage configurations
```

---

## ⚡ Prerequisites & Package Dependencies

Ensure Python 3.10+ is installed on your local environment. Create a `requirements.txt` containing:

```text
fastapi
uvicorn
chromadb
sentence-transformers
pydantic
python-dotenv
sqlalchemy
google-genai
ollama
```

Install the requirements:
```bash
pip install -r requirements.txt
```

### Setting up the Local Fallback Engine
1. Download and run the **Ollama** desktop environment from [ollama.com](https://ollama.com).
2. Pull the designated local backup weights model through your terminal prompt:
   ```bash
   ollama pull llama3.1
   ```

---

## 🛠️ Configuration & Secrets Injection

Generate a `.env` file within the root working folder directory matching this structure:

```env
GEMINI_API_KEY=AIzaSyYourVerifiedGoogleCloudGeminiDeveloperTokenHere
```

---

## 🚀 Execution & Simulation Runbook

### 1. Pre-populate Storage Registers (Simulation Data Seeding)
Execute the multi-profile data ingestion engine to synchronize 14 rich testing assets simultaneously inside SQLite indexes and ChromaDB semantic spaces:

```bash
python seed_data.py
```

### 2. Initiate the Network API Core
Boot up the FastAPI gateway cluster managed through the Uvicorn runtime server:

```bash
uvicorn main:app --reload
```
* **Interactive Endpoint Registry (Swagger UI)**: Open `http://127.0.0` inside your preferred browser.

### 3. Verify Auditing Tables
Track internal application execution paths, elapsed time profiles, and engine logging behaviors recorded inside the relational platform tables:

```bash
python check_logs.py
```

---

## 📡 Core API Specification Endpoints

### Ingest New Property Record
* **Endpoint**: `POST /api/v3/properties`
* **Payload Structure (`application/json`)**:
```json
{
  "doc_id": "PROP-999",
  "text": "Stunning architectural luxury penthouse with beach front views.",
  "price": 2400000.0,
  "location": "Malibu, CA",
  "property_type": "Penthouse"
}
```

### Execute Context-Aware Advisory Queries
* **Endpoint**: `POST /api/v3/advise`
* **Payload Structure (`application/json`)**:
```json
{
  "question": "Show me high-end properties with a boat dock for a yacht."
}
```
* **Output Matrix Structure (`application/json`)**:
```json
{
  "advice": "Based on the verified context, you should review the Miami property which includes a private boat dock for \$12,500,000.",
  "engine": "gemini",
  "sources": 3
}
```
