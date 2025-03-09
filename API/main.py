from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from Doorlock import DoorLock
from datetime import datetime, timedelta
import uvicorn
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

door_lock = DoorLock()
closing_time = None

connected_clients = []

class KeyModel(BaseModel):
    key: str
    
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_close())
    
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down")
    for client in connected_clients:
        await client.send_text("exit")


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
    
    for client in connected_clients:
        if door_lock.is_locked() == False:
            await client.send_text("lock")
            
    await asyncio.sleep(1)
        
    door_lock.lock()

    return {"message": "Tür verriegelt"}

@app.post("/unlock")
async def unlock_door():
    global closing_time
    
    for client in connected_clients:
        if door_lock.is_locked():
            await client.send_text("unlock")
            closing_time = datetime.now() + timedelta(seconds=door_lock.get_opentime())
            
    await asyncio.sleep(1)
            
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
    
    for client in connected_clients:
        if pin_status == True:
            await unlock_door()
        elif pin_status == False and door_lock.get_length() == 4:
            await client.send_text("false")
        else:
            length = door_lock.get_length()
            await client.send_text(f"key{length}")
            
    door_lock.reset_code()
    
    return {"pin": door_lock.code, "status": pin_status}
    
@app.post("/reset_pin")
async def reset_pin():
    door_lock.reset_code()
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print("Device connected")

    try:
        while True:
            message = await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Device disconnected")
        
async def auto_close():
    global closing_time
    while True:
        now = datetime.now()
        if closing_time == None:
            await asyncio.sleep(1)
            continue
        if now >= closing_time:
            if door_lock.is_locked() == False:
                await lock_door()
            closing_time = None
        await asyncio.sleep(1)

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)