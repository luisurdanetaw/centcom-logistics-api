from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controller import user_controller

app = FastAPI()

origins = [
    "http://localhost:3000",  # Replace with the origin of your frontend (e.g., http://yourfrontend.com)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "CENTCOM Logistics API"}

app.include_router(user_controller.router, prefix="/user")
