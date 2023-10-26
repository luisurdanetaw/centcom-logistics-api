from pydantic import BaseModel

class User(BaseModel):
    id: int = 0
    first_name: str = "NULL"
    last_name: str = "NULL"
    position: str = "NULL"
    email: str = "NULL"
    password: str ="NULL"
    phone: str = "NULL"