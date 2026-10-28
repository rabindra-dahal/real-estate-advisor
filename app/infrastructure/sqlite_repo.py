from sqlalchemy import create_engine, Column, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import List, Optional
import datetime
from app.interfaces.relational_repo import IRelationalRepository
from app.domain.entities import ErrorLog, Property, AdviceLog, ChatMessage

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

class DBChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(String, primary_key=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class DBErrorLog(Base):
    __tablename__ = "error_logs"
    id = Column(String, primary_key=True)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

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

    def save_message(self, message: ChatMessage):
        with self.SessionLocal() as session:
            db_msg = DBChatMessage(id=message.message_id, session_id=message.session_id, role=message.role, content=message.content, timestamp=message.timestamp)
            session.add(db_msg)
            session.commit()

    def get_session_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        with self.SessionLocal() as session:
            db_messages = session.query(DBChatMessage)\
                                 .filter(DBChatMessage.session_id == session_id)\
                                 .order_by(DBChatMessage.timestamp.asc())\
                                 .suffix_with(f"LIMIT {limit}")\
                                 .all()
            return [ChatMessage(m.id, m.session_id, m.role, m.content, m.timestamp) for m in db_messages]

    def delete_session_history(self, session_id: str) -> int:
        with self.SessionLocal() as session:
            deleted_count = session.query(DBChatMessage)\
                                   .filter(DBChatMessage.session_id == session_id)\
                                   .delete(synchronize_session=False)
            session.commit()
            return deleted_count
    
    def save_error_log(self, error: ErrorLog):
        with self.SessionLocal() as session:
            db_error = DBErrorLog(
                id=error.log_id,
                endpoint=error.endpoint,
                method=error.method,
                error_message=error.error_message,
                stack_trace=error.stack_trace,
                timestamp=error.timestamp
            )
            session.add(db_error)
            session.commit()
