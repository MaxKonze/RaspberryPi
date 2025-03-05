from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from Doorlock import DoorLock
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

door_lock = DoorLock()

class KeyModel(BaseModel):
    key: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    
    if door_lock.is_locked() == True:
        return RedirectResponse("/locked")
    
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/status")
async def get_status():
    return {"locked": door_lock.is_locked()}

@app.get("/lock")
async def lock_door():
    
    door_lock.lock()
    
    return {"message": "Tür verriegelt"}

@app.post("/unlock")
async def unlock_door():
    
    door_lock.unlock()
    return {"message": "Tür entriegelt"}

@app.get("/status-page", response_class=HTMLResponse)
async def status_page(request: Request):
    
    if door_lock.is_locked() == True:
        return RedirectResponse("/locked")
    
    return templates.TemplateResponse("status.html", {"request": request, "locked": door_lock.is_locked()})

@app.get("/locked", response_class=HTMLResponse)
async def locked_page(request: Request):
    
    if door_lock.is_locked() == False:
        return RedirectResponse("/")
    
    return templates.TemplateResponse("locked.html", {"request": request})

@app.post("/key")
async def handle_key(key_model: KeyModel):
    
    key = key_model.key
    
    door_lock.update_code(key)
    pin_status = door_lock.checkPin()
    
    return {"pin": door_lock.code, "status": pin_status}
    
@app.post("/reset_pin")
async def reset_pin():
    door_lock.reset_code()
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)