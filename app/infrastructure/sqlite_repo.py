from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, String, Float, Text, DateTime, select, delete
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
    def __init__(self, db_url: str = "sqlite+aiosqlite:///./clean_real_estate.db"):
        self.engine = create_async_engine(db_url, connect_args={"check_same_thread": False})
        self.AsyncSessionLocal = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def init_db(self):
        """Asynchronously sets up the base relational database schema tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save_property(self, prop: Property):
        async with self.AsyncSessionLocal() as session:
            db_prop = DBProperty(id=prop.doc_id, text=prop.text, price=prop.price, location=prop.location, property_type=prop.property_type, created_at=prop.created_at)
            session.add(db_prop)
            await session.commit()

    async def get_property(self, doc_id: str) -> Optional[Property]:
        async with self.AsyncSessionLocal() as session:
            result = await session.execute(select(DBProperty).filter(DBProperty.id == doc_id))
            db_prop = result.scalars().first()
            if not db_prop: return None
            return Property(db_prop.id, db_prop.text, db_prop.price, db_prop.location, db_prop.property_type, db_prop.created_at)

    async def save_advice_log(self, log: AdviceLog):
        async with self.AsyncSessionLocal() as session:
            db_log = DBAdviceLog(id=log.log_id, question=log.question, answer=log.answer, provider_used=log.provider_used, timestamp=log.timestamp)
            session.add(db_log)
            await session.commit()

    async def save_message(self, message: ChatMessage):
        async with self.AsyncSessionLocal() as session:
            db_msg = DBChatMessage(id=message.message_id, session_id=message.session_id, role=message.role, content=message.content, timestamp=message.timestamp)
            session.add(db_msg)
            await session.commit()

    async def get_session_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        async with self.AsyncSessionLocal() as session:
            query = select(DBChatMessage).filter(DBChatMessage.session_id == session_id).order_by(DBChatMessage.timestamp.asc()).limit(limit)
            result = await session.execute(query)
            db_messages = result.scalars().all()
            return [ChatMessage(m.id, m.session_id, m.role, m.content, m.timestamp) for m in db_messages]
    
    async def delete_session_history(self, session_id: str) -> int:
        async with self.AsyncSessionLocal() as session:
            deleted_count = session.query(DBChatMessage)\
                                   .filter(DBChatMessage.session_id == session_id)\
                                   .delete(synchronize_session=False)
            await session.commit()
            return deleted_count
    
    async def save_error_log(self, error: ErrorLog):
        async with self.AsyncSessionLocal() as session:
            db_error = DBErrorLog(id=error.log_id, endpoint=error.endpoint, method=error.method, error_message=error.error_message, stack_trace=error.stack_trace, timestamp=error.timestamp)
            session.add(db_error)
            await session.commit()

    async def get_recent_errors(self, limit: int = 10) -> List[ErrorLog]:
        """Fetches recent error log records sorted chronologically descending."""
        async with self.AsyncSessionLocal() as session:
            # Build the async-compatible select statement
            stmt = (
                select(DBErrorLog)
                .order_by(DBErrorLog.timestamp.desc())
                .limit(limit)
            )
            
            # Await the database execution
            result = await session.execute(stmt)
            
            # Extract the ORM objects out of the result rows
            db_errors = result.scalars().all()
            
            return [
                ErrorLog(e.id, e.endpoint, e.method, e.error_message, e.stack_trace, e.timestamp)
                for e in db_errors
            ]


    async def get_error_by_id(self, log_id: str) -> Optional[ErrorLog]:
        """Retrieves a single error log signature by its distinct tracking code."""
        async with self.AsyncSessionLocal() as session:
            # Optimised for primary key lookups in AsyncSession
            e = await session.get(DBErrorLog, log_id)
            
            if not e: 
                return None
                
            return ErrorLog(e.id, e.endpoint, e.method, e.error_message, e.stack_trace, e.timestamp)

    async def clear_all_error_logs(self) -> int:
        async with self.AsyncSessionLocal() as session:
            # Build the delete statement
            stmt = delete(DBErrorLog)
            
            # Execute the deletion statement
            result = await session.execute(stmt)
            
            # Await the commit to persist changes in the database
            await session.commit()
            
            # Return the total number of deleted rows
            return result.rowcount


