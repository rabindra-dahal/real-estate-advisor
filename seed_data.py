import os
import time
from dotenv import load_dotenv
from app.infrastructure.sqlite_repo import SQLiteRepository
from app.infrastructure.chroma_repo import ChromaRepository
from app.use_cases.ingest_property import IngestPropertyUseCase

def run_simulation():
    print(" Initializing Expanded Real Estate Simulation Dataset...")
    load_dotenv()

    # Initialize Layers
    sqlite_repo = SQLiteRepository()
    chroma_repo = ChromaRepository()

    ingest_use_case = IngestPropertyUseCase(sqlite_repo, chroma_repo)

    # 14 Diverse Property Records (Structured + Unstructured descriptions)
    expanded_dataset = [
        {
            "doc_id": "PROP-001",
            "text": "Stunning 3-bedroom luxury penthouse in Downtown Manhattan. Features floor-to-ceiling windows, panoramic city skyline views, wrap-around balcony, smart automation, and private elevator access. Close to premier fine dining and transit hubs.",
            "price": 4500000.0, "location": "New York, NY", "property_type": "Penthouse"
        },
        {
            "doc_id": "PROP-002",
            "text": "Charming mid-century modern single-family home in Austin. Offers 4 bedrooms, 2.5 baths, an upgraded open-concept kitchen, and a spacious landscaped backyard complete with an inground pool. Excellent school district location.",
            "price": 875000.0, "location": "Austin, TX", "property_type": "House"
        },
        {
            "doc_id": "PROP-003",
            "text": "Modern industrial loft space in downtown Chicago. Exposed brick walls, timber ceilings, 1 bedroom, 1.5 bathrooms. Secure basement parking garage included. Ideal corporate rental option or minimalist living layout.",
            "price": 620000.0, "location": "Chicago, IL", "property_type": "Loft"
        },
        {
            "doc_id": "PROP-004",
            "text": "Massive commercial warehouse facility situated near international freight corridors in Atlanta. High bay clearance ceilings, 6 loading docks, heavy electrical infrastructure, and attached administrative office spaces.",
            "price": 3100000.0, "location": "Atlanta, GA", "property_type": "Commercial"
        },
        {
            "doc_id": "PROP-005",
            "text": "Affordable starter studio apartment in Queens. Compact layout with updated kitchen appliances, large storage closet, and immediate access to the subway. Maintenance fees include heating and water utilities. Perfect for first-time buyers.",
            "price": 320000.0, "location": "Queens, NY", "property_type": "Apartment"
        },
        {
            "doc_id": "PROP-006",
            "text": "Cozy rustic suburban home with 3 bedrooms and a wrap-around porch. Features a detached 2-car garage, hardwood flooring throughout, and a wood-burning fireplace. Located in a quiet cul-de-sac with mature trees.",
            "price": 410000.0, "location": "Nashville, TN", "property_type": "House"
        },
        {
            "doc_id": "PROP-007",
            "text": "Ultra-modern luxury waterfront villa in Miami Beach. 6 bedrooms, 7.5 bathrooms, private boat dock, infinity pool overlooking the bay, and a custom chef's kitchen. Gated community with 24/7 high-profile security presence.",
            "price": 12500000.0, "location": "Miami, FL", "property_type": "Villa"
        },
        {
            "doc_id": "PROP-008",
            "text": "Prime downtown retail storefront property with high foot traffic. Features large display windows, open commercial floor plan, back inventory storage room, and updated HVAC systems. Great investment opportunity.",
            "price": 1850000.0, "location": "Boston, MA", "property_type": "Commercial"
        },
        {
            "doc_id": "PROP-009",
            "text": "Fixer-upper single-family house with massive investment potential. Requires structural roof repairs and cosmetic interior remodeling. Large corner lot size. Being sold completely as-is, great flip opportunity for contractors.",
            "price": 1950000.0, "location": "San Francisco, CA", "property_type": "House"
        },
        {
            "doc_id": "PROP-010",
            "text": "Luxury high-rise condo on the 32nd floor in Los Angeles. 2 bedrooms, 2 bathrooms, marble bathrooms, concierge service, rooftop fitness gym access, and valet parking. Breathtaking views of the city hills.",
            "price": 1450000.0, "location": "Los Angeles, CA", "property_type": "Condo"
        },
        {
            "doc_id": "PROP-011",
            "text": "Eco-friendly modern townhome featuring solar panels, geothermal heating, and a green roof garden deck. 3 levels of living space, attached garage with EV charging station, energy-efficient smart appliances included.",
            "price": 750000.0, "location": "Denver, CO", "property_type": "Townhouse"
        },
        {
            "doc_id": "PROP-012",
            "text": "Spacious family suburban house in Seattle. 5 bedrooms, 4 bathrooms, fully finished basement configured as a home theater, large back deck, and beautifully manicured gardens bordering a peaceful greenbelt.",
            "price": 1150000.0, "location": "Seattle, WA", "property_type": "House"
        },
        {
            "doc_id": "PROP-013",
            "text": "Budget-friendly 2-bedroom garden-style condominium. Low monthly HOA fees, community swimming pool privileges, shared laundry facilities, and a private covered parking space. Close to local community colleges.",
            "price": 245000.0, "location": "Phoenix, AZ", "property_type": "Condo"
        },
        {
            "doc_id": "PROP-014",
            "text": "Secluded luxury mountain log cabin estate spread across 5 acres of private pine forest. Features exposed log beams, floor-to-ceiling stone fireplace, wrap-around deck with a hot tub, and panoramic mountain pass vistas.",
            "price": 2200000.0, "location": "Aspen, CO", "property_type": "Cabin"
        }
    ]

    print("\n Ingesting Data into SQLite and ChromaDB...")
    for prop in expanded_dataset:
        try:
            entity = ingest_use_case.execute(
                doc_id=prop["doc_id"],
                text=prop["text"],
                price=prop["price"],
                location=prop["location"],
                property_type=prop["property_type"]
            )
            print(f"  Saved {entity.doc_id} -> {entity.location} (${entity.price:,.0f})")
        except ValueError:
            print(f"  {prop['doc_id']} already exists in databases. Skipping.")

    print("\n Bulk data seeding completed! You can now query your API or run simulations.")

if __name__ == "__main__":
    run_simulation()

"""
• Add conversational memory tracking to the database
• Implement asynchronous API processing for higher performance
• Write a suite of automated unit tests for the use cases

"""
