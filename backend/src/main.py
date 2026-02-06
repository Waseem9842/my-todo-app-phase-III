from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.task_router import task_router
from src.api.auth_router import auth_router
from src.api.health_endpoints import router as health_router
from src.api.chat_endpoints import router as chat_router
from src.database.database import create_db_and_tables
from src.config.app_config import app_config
import uvicorn
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="A simple todo API for managing user tasks",
    version="1.0.0",
    debug=app_config.debug
)

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if app_config.debug else [],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth router first (without user_id in path)
app.include_router(auth_router, prefix="/api", tags=["auth"])

# Include the health router for system monitoring
app.include_router(health_router, prefix="", tags=["health"])

# Include the chat router (with user_id in path)
app.include_router(chat_router, prefix="", tags=["chat"])

# Include the task router (with user_id in path)
app.include_router(task_router, prefix="/api/{user_id}", tags=["tasks"])

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    create_db_and_tables()
    logger.info("Database initialized.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)