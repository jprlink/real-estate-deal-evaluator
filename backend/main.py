"""
Main entry point for FastAPI application.

Run with: python -m uvicorn backend.main:app --reload
Access at: http://localhost:8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Real Estate Deal Evaluator",
    description="AI-powered Paris real estate investment analysis",
    version="0.1.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # Production
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "ok",
        "message": "Real Estate Deal Evaluator API",
        "version": "0.1.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "evaluate": "/api/evaluate",
            "parse_pdf": "/api/parse/pdf",
            "research": "/api/research",
            "negotiate": "/api/negotiate"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Import and include routers
from backend.api.routes import evaluate, parse

app.include_router(evaluate.router, prefix="/api", tags=["evaluate"])
app.include_router(parse.router, prefix="/api", tags=["parse"])

# Serve frontend static files if they exist
frontend_build = os.path.join(os.path.dirname(__file__), "../frontend/build")
if os.path.exists(frontend_build):
    app.mount("/", StaticFiles(directory=frontend_build, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)