from fastapi import FastAPI
from controller import user_controller

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "CENTCOM Logistics API"}

app.include_router(user_controller.router, prefix="/user")
