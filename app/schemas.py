from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class AlertCreate(BaseModel):
    event: Optional[str]
    sent_at: Optional[datetime]
    raw: Any
