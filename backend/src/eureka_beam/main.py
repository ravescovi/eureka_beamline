"""Main FastAPI application module for the Eureka Beamline backend service.

This module serves as the entry point for the FastAPI application, setting up
the server configuration, middleware, and routing for all agent endpoints.
"""

from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import ioc_router

app = FastAPI(
    title="Eureka Beamline API",
    description="API service for Eureka Beamline agents and tools",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint returning API status.
    
    Returns:
        Dict[str, Any]: A dictionary containing the API status and version.
    """
    return {
        "status": "online",
        "version": "0.1.0",
        "service": "eureka-beamline-api"
    }

@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint for monitoring and container orchestration.
    
    Returns:
        JSONResponse: A JSON response indicating the service health status.
    """
    return JSONResponse(
        content={"status": "healthy"},
        status_code=200
    )

# Include routers
app.include_router(ioc_router.router, prefix="/agents", tags=["agents"]) 