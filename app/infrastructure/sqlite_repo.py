from sqlalchemy import create_engine, Column, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from app.interfaces.relational_repo import IRelationalRepository
from app.domain.entities import Property, AdviceLog

Base = declarative_base()

class DBProperty(Base):
    __tablename__ = "properties"
    id = Column(String, primary_key=True)
    text = Column(Text)
    price = Column(Float)
    location = Column(String)
    property_type = Column(String)
    created_at = Column(DateTime)

class DBAdviceLog(Base):
    __tablename__ = "advice_logs"
    id = Column(String, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    provider_used = Column(String)
    timestamp = Column(DateTime)

class SQLiteRepository(IRelationalRepository):
    def __init__(self, db_url: str = "sqlite:///./clean_real_estate.db"):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def save_property(self, prop: Property):
        with self.SessionLocal() as session:
            db_prop = DBProperty(id=prop.doc_id, text=prop.text, price=prop.price, location=prop.location, property_type=prop.property_type, created_at=prop.created_at)
            session.add(db_prop)
            session.commit()

    def get_property(self, doc_id: str):
        with self.SessionLocal() as session:
            db_prop = session.query(DBProperty).filter(DBProperty.id == doc_id).first()
            if not db_prop: return None
            return Property(db_prop.id, db_prop.text, db_prop.price, db_prop.location, db_prop.property_type, db_prop.created_at)

    def save_advice_log(self, log: AdviceLog):
        with self.SessionLocal() as session:
            db_log = DBAdviceLog(id=log.log_id, question=log.question, answer=log.answer, provider_used=log.provider_used, timestamp=log.timestamp)
            session.add(db_log)
            session.commit()
