from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from .db import Base
from datetime import datetime


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    nws_id = Column(String, unique=True, index=True, nullable=False)

    # Core fields
    event = Column(String, index=True, nullable=True)
    eventcode = Column(String, index=True, nullable=True)
    headline = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    instruction = Column(Text, nullable=True)

    # status and metadata
    status = Column(String, index=True, nullable=True)
    message_type = Column(String, nullable=True)
    category = Column(String, nullable=True)
    severity = Column(String, index=True, nullable=True)
    certainty = Column(String, nullable=True)
    urgency = Column(String, nullable=True)

    # sender info
    sender = Column(String, nullable=True)
    sender_name = Column(String, nullable=True)

    # timestamps
    sent_at = Column(DateTime, index=True, nullable=True)
    effective_at = Column(DateTime, index=True, nullable=True)
    onset_at = Column(DateTime, index=True, nullable=True)
    expires_at = Column(DateTime, index=True, nullable=True)
    ends_at = Column(DateTime, index=True, nullable=True)
    updated_at = Column(DateTime, index=True, nullable=True)

    # geospatial / related
    area_desc = Column(Text, nullable=True)
    geocode = Column(JSONB, nullable=True)
    affected_zones = Column(JSONB, nullable=True)
    references = Column(JSONB, nullable=True)

    # other fields
    response = Column(String, nullable=True)
    parameters = Column(JSONB, nullable=True)
    scope = Column(String, nullable=True)
    code = Column(String, nullable=True)
    language = Column(String, nullable=True)
    web = Column(String, nullable=True)

    # raw JSON plus fetch metadata
    raw = Column(JSONB)


class SeverityEmoji(Base):
    __tablename__ = "severity_emoji"
    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String, unique=True, index=True, nullable=False)
    emoji = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class PhenomenonEmoji(Base):
    __tablename__ = "phenomenon_emoji"
    id = Column(Integer, primary_key=True, index=True)
    phenomenon = Column(String, unique=True, index=True, nullable=False)
    emoji = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

