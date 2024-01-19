from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseDTO(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
