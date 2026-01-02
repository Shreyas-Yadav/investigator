"""Transcription API endpoints."""

import os
import tempfile
import shutil
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from services.youtube import extract_video_id, get_video_info, download_audio
from services.transcription import get_transcript, get_youtube_transcript

router = APIRouter(prefix="/api", tags=["transcription"])


class TranscribeRequest(BaseModel):
    url: str


class TranscribeResponse(BaseModel):
    video_id: str
    title: str
    channel: str
    duration: int
    transcript: str
    segments: list[dict]
    source: str  # 'youtube_captions' or 'whisper'


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_video(request: TranscribeRequest):
    """
    Extract transcript from a YouTube video.
    
    Tries YouTube captions first (fast), falls back to Whisper (slower but works for all videos).
    """
    # Extract video ID
    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL. Please provide a valid YouTube video link."
        )
    
    # Get video metadata
    try:
        video_info = get_video_info(video_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Could not fetch video info. The video may be private or unavailable. Error: {str(e)}"
        )
    
    # Try YouTube captions first (fast path - no download needed)
    transcript_result = get_youtube_transcript(video_id)
    
    if transcript_result:
        return TranscribeResponse(
            video_id=video_id,
            title=video_info['title'],
            channel=video_info['channel'],
            duration=video_info['duration'],
            transcript=transcript_result['text'],
            segments=transcript_result['segments'],
            source=transcript_result['source'],
        )
    
    # Fall back to Whisper - need to download audio
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        
        # Download audio
        audio_path = download_audio(video_id, temp_dir)
        
        # Transcribe with Whisper
        transcript_result = get_transcript(video_id, audio_path)
        
        return TranscribeResponse(
            video_id=video_id,
            title=video_info['title'],
            channel=video_info['channel'],
            duration=video_info['duration'],
            transcript=transcript_result['text'],
            segments=transcript_result['segments'],
            source=transcript_result['source'],
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to transcribe video: {str(e)}"
        )
    
    finally:
        # Cleanup temp directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "investigator-backend"}
