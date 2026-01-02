"""Investigator Backend - YouTube Transcript Extraction API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.transcribe import router as transcribe_router

app = FastAPI(
    title="Investigator API",
    description="YouTube video transcript extraction and fact-checking",
    version="0.1.0",
)

# CORS middleware - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcribe_router)


@app.get("/")
async def root():
    return {
        "message": "Investigator API",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
