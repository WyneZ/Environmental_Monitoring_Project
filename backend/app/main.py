from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.api import auth, users, devices, sensors, nimble
from app.api.nimble import router as nimble_router
from app.api.rooms import router as rooms_router
from app.api.devices import router as devices_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nimble_router, prefix="/nimble", tags=["nimble"])
app.include_router(rooms_router, prefix="/rooms", tags=["rooms"])
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(devices.router, prefix="/devices", tags=["devices"])
# app.include_router(sensors.router, prefix="/sensors", tags=["sensors"])

# Optional: event handlers, middleware, etc.
