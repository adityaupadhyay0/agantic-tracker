from sqlalchemy import Column, String, DateTime, JSON, Float, Enum as SQLEnum
from app.db.base import Base
import uuid
from app.schemas.bco import BCOScope, BCOType

class BCOModel(Base):
    __tablename__ = "bcos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scope = Column(SQLEnum(BCOScope))
    scope_id = Column(String, index=True)
    type = Column(SQLEnum(BCOType))
    label = Column(String)
    evidence = Column(JSON)
    confidence = Column(Float)
    temporal_json = Column(JSON)
    context_json = Column(JSON)
    version = Column(String)
    lineage = Column(JSON)
