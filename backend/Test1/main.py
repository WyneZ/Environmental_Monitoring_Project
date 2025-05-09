from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import BaseModel
import motor.motor_asyncio

app = FastAPI()

# MongoDB setup
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = client["test_db"]
collection = db["messages"]

# CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# WebSocket connections
clients = []

class Message(BaseModel):
    text: str

@app.post("/submit")
async def submit_message(msg: Message):
    # Store in MongoDB
    await collection.insert_one({"text": msg.text})
    
    # Notify all connected WebSocket clients
    for client in clients:
        await client.send_text(msg.text)
    
    return {"status": "success", "text": msg.text}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        # On connection, send existing messages
        existing = await collection.find().to_list(100)
        for item in existing:
            await websocket.send_text(item["text"])

        # Keep alive
        while True:
            await websocket.receive_text()  # dummy read to keep connection open
    except WebSocketDisconnect:
        clients.remove(websocket)
