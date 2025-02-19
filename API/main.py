from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class LockStatus(BaseModel):
    locked: bool

@app.get("/")
async def root():
    return {"message": "Willkommen zur Smart Door Lock API"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/status")
async def get_status():
    return {"locked": False}

@app.get("/lock")
async def lock_door():
    return {"message": "Tür verriegelt"}

@app.post("/unlock")
async def unlock_door():
    return {"message": "Tür entriegelt"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
