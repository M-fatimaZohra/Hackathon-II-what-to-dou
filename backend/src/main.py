from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import tasks
from src.api import chat
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Get environment mode
environment = os.getenv("ENVIRONMENT", "development")

# Configure FastAPI based on environment
if environment == 'production':
    # In production, disable docs and restrict CORS
    app = FastAPI(
        title="Todo API",
        version="1.0.0",
        docs_url=None,  # Disable /docs
        redoc_url=None  # Disable /redoc
    )
    # Use production frontend URL
    frontend_url = os.getenv("FRONTEND_API_URL", "https://hackathon-ii-what-to-dou.vercel.app")
    # For production, only allow the single frontend URL
    origins = [frontend_url]
else:
    # In development, enable docs and allow localhost
    app = FastAPI(title="Todo API", version="1.0.0")
    # Use development frontend URL
    frontend_url = os.getenv("FRONTEND_API_URL", "http://localhost:3000")
    # For development, allow both localhost variants for frontend flexibility
    origins = [frontend_url, "http://127.0.0.1:3000"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow multiple frontend URLs in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers for ChatKit SDK compatibility
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
