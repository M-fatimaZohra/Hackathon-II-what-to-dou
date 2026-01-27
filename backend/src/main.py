from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import tasks
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
frontend_url = os.getenv("FRONTEND_API_URL", "http://localhost:3000")  # Use the frontend URL from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # Allow frontend URL from environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],  # Only allow necessary headers
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
