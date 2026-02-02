from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.event_bus import event_bus
import json
from app.config import USERS_FILE
from app.core.vector_store import vector_store
from app.core.notification_handler import handle_job_search_event
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup logic
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        await vector_store.add_documents(users)
        print(f"LIFESPAN: Successfully indexed {len(users)} candidates.")
    except Exception as e:
        print(f"LIFESPAN ERROR: {e}")
    
    yield
    # Shutdown logic (optional)

app = FastAPI(lifespan=lifespan)

# Logging Middleware
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router)

# Register event handler
event_bus.subscribe("JOB_SEARCH", handle_job_search_event)
