from pydantic import BaseModel
from datetime import date
from typing import Optional

class TMR(BaseModel):
    id: int = 0
    requestor_id: Optional[int] = None
    cargo_description: Optional[str] = None
    quantity: Optional[str] = None
    units: Optional[str] = None
    id_num: Optional[str] = None
    requestor: Optional[str] = None
    date_received: Optional[str] = None
