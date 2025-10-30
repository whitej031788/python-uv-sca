from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.routers import auth


DEBUG = True

app = FastAPI(
    title="Vulnerable FastAPI App",
    description="SonarQube Workshop Sample Application",
    version="1.0.0",
    debug=DEBUG  # Should not be hardcoded
)

# Overly permissive CORS - Security Issue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Should be specific methods
    allow_headers=["*"],  # Should be specific headers
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])

if __name__ == "__main__":
    # Running with debug and auto-reload in production - Security Issue
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Binding to all interfaces - potential security issue
        port=8000,
        reload=True,  # Auto-reload in production
        ssl_keyfile=None,  # No HTTPS enforcement
        ssl_certfile=None
    )

def canary():
    am_i_being_scanned = "?"
    return