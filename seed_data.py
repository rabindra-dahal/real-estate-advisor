import os
import time
from dotenv import load_dotenv
from app.infrastructure.sqlite_repo import SQLiteRepository
from app.infrastructure.chroma_repo import ChromaRepository
from app.infrastructure.gemini_service import GeminiService
from app.infrastructure.ollama_service import OllamaService
from app.use_cases.ingest_property import IngestPropertyUseCase
from app.use_cases.query_advisor import QueryAdvisorUseCase

def run_simulation():
    print(" Initializing Clean Architecture Real Estate Simulation Ecosystem...")
    load_dotenv()

    # 1. Initialize Adapters & Use Cases
    sqlite_repo = SQLiteRepository()
    chroma_repo = ChromaRepository()

    ingest_use_case = IngestPropertyUseCase(sqlite_repo, chroma_repo)

    # 2. Mock Dataset (Structured & Unstructured Property Listings)
    sample_properties = [
        {
            "doc_id": "PROP-001",
            "text": "Stunning 3-bedroom luxury penthouse in Downtown Manhattan. Features floor-to-ceiling windows, panoramic city skyline views, wrap-around balcony, smart automation, and private elevator access. Close to premier fine dining and transit hubs.",
            "price": 4500000.0,
            "location": "Downtown Manhattan, NY",
            "property_type": "Penthouse"
        },
        {
            "doc_id": "PROP-002",
            "text": "Charming mid-century modern single-family home in Austin. Offers 4 bedrooms, 2.5 baths, an upgraded open-concept kitchen, and a spacious landscaped backyard complete with an inground pool. Excellent school district location.",
            "price": 875000.0,
            "location": "Austin, TX",
            "property_type": "House"
        },
        {
            "doc_id": "PROP-003",
            "text": "Modern industrial loft space in downtown Chicago. Exposed brick walls, timber ceilings, 1 bedroom, 1.5 bathrooms. Secure basement parking garage included. Ideal corporate rental option or minimalist living layout.",
            "price": 620000.0,
            "location": "Chicago, IL",
            "property_type": "Loft"
        },
        {
            "doc_id": "PROP-004",
            "text": "Massive commercial warehouse facility situated near international freight corridors in Atlanta. High bay clearance ceilings, 6 loading docks, heavy electrical infrastructure, and attached administrative office spaces.",
            "price": 3100000.0,
            "location": "Atlanta, GA",
            "property_type": "Commercial"
        }
    ]

    # 3. Simulate Ingestion Engine
    print("\n Phase 1: Seeding Properties into Database Repositories...")
    for prop in sample_properties:
        try:
            entity = ingest_use_case.execute(
                doc_id=prop["doc_id"],
                text=prop["text"],
                price=prop["price"],
                location=prop["location"],
                property_type=prop["property_type"]
            )
            print(f"  Successfully synchronized {entity.doc_id} to SQLite & ChromaDB ({entity.property_type})")
        except ValueError as e:
            print(f"  Skipping {prop['doc_id']}: {str(e)}")

    # sample_queries = [
    #     "Find me a luxury high-end property in Manhattan with skyline views and a private elevator.",
    #     "What properties do you have under one million dollars suitable for a family near good schools?",
    #     "Are there any industrial lofts available with exposed brick features?",
    #     "I need a commercial facility with high bay clearance and loading docks."
    # ]
    print("\n Simulation completed successfully! Check your SQLite `clean_real_estate.db` file to review persisted system audit records.")

if __name__ == "__main__":
    run_simulation()
