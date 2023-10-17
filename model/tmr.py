from pydantic import BaseModel
from datetime import date

class Tmr(BaseModel):
    id_num: str
    unit_name: str
    requestor: str
    date_received: date
    date_approved: date
    status: str
    carrier: str
    weight: int
    containers: int
    #we need to add RLD, ALD, RDD, ADD 

