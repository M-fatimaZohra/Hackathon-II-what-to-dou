from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import tasks

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific origin for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
