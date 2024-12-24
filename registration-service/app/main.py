from fastapi import FastAPI
from app.routes import router

app = FastAPI()

app.include_router(router, prefix="/api/registrations", tags=["Registrations"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Registration Service API"}
