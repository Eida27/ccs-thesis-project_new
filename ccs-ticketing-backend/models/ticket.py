from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from core.database import Base

class DBTicket(Base):
    __tablename__ = "tickets"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Ingestion Data (From Next.js)
    location = Column(String, index=True)
    description = Column(Text)
    
    # AI Triage Data (From OpenAI)
    ai_category = Column(String, index=True)
    ai_sentiment = Column(String)
    priority_score = Column(Integer, index=True)
    
    # Lifecycle Data
    status = Column(String, default="Open") # Open, Assigned, Resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True) # Used later for "Time-to-Resolve" metric