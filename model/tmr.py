from pydantic import BaseModel
from datetime import date

class Tmr(BaseModel):
    id_num: str
    location: str
    unit_name: str
    requestor: str
    date_received: date
    date_approved: date
    status: str
    carrier: str
    weight: int
    containers: int
    pieces: int

    cargo_description: str
    cargo_class: str
    move: str
    origin: str
    destination: str
    pre_transit: str
    rld: date
    rdd: date
    post_transit: str

