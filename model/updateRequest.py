from pydantic import BaseModel

class updateRequest(BaseModel):
    facility_id: int = 0
    item_name: str = "NULL"
    quantity: int = "NULL"