"""Transcription service - YouTube captions first, Whisper fallback."""

import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)
import whisper

# Global whisper model (loaded lazily)
_whisper_model = None


def get_whisper_model(model_name: str = "base"):
    """Load Whisper model (cached after first load)."""
    global _whisper_model
    if _whisper_model is None:
        print(f"Loading Whisper model '{model_name}'... (this may take a moment)")
        _whisper_model = whisper.load_model(model_name)
        print("Whisper model loaded!")
    return _whisper_model


def get_youtube_transcript(video_id: str) -> dict | None:
    """
    Try to fetch existing YouTube captions.
    
    Returns:
        dict with 'text' and 'segments' if available, None otherwise
    """
    try:
        # Try to get transcript in preferred languages
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Prefer manual transcripts, then auto-generated
        try:
            transcript = transcript_list.find_manually_created_transcript(['en', 'hi', 'es', 'fr', 'de'])
        except:
            try:
                transcript = transcript_list.find_generated_transcript(['en', 'hi', 'es', 'fr', 'de'])
            except:
                # Get any available transcript
                transcript = next(iter(transcript_list))
        
        segments = transcript.fetch()
        
        # Combine all text
        full_text = " ".join([seg['text'] for seg in segments])
        
        return {
            'text': full_text,
            'segments': [
                {
                    'start': seg['start'],
                    'duration': seg['duration'],
                    'text': seg['text'],
                }
                for seg in segments
            ],
            'source': 'youtube_captions',
        }
    
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return None
    except Exception as e:
        print(f"YouTube transcript error: {e}")
        return None


def transcribe_with_whisper(audio_path: str, model_name: str = "base") -> dict:
    """
    Transcribe audio file using local Whisper model.
    
    Args:
        audio_path: Path to audio file
        model_name: Whisper model size (tiny, base, small, medium, large)
    
    Returns:
        dict with 'text' and 'segments'
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    model = get_whisper_model(model_name)
    
    print(f"Transcribing audio with Whisper...")
    result = model.transcribe(audio_path)
    
    return {
        'text': result['text'].strip(),
        'segments': [
            {
                'start': seg['start'],
                'duration': seg['end'] - seg['start'],
                'text': seg['text'].strip(),
            }
            for seg in result.get('segments', [])
        ],
        'source': 'whisper',
        'language': result.get('language', 'unknown'),
    }


def get_transcript(video_id: str, audio_path: str | None = None) -> dict:
    """
    Get transcript using the best available method.
    
    Strategy:
    1. Try YouTube captions (instant, no download needed)
    2. Fall back to Whisper (requires audio file)
    
    Args:
        video_id: YouTube video ID
        audio_path: Path to audio file (required for Whisper fallback)
    
    Returns:
        dict with 'text', 'segments', and 'source'
    """
    # Try YouTube captions first (fast path)
    result = get_youtube_transcript(video_id)
    if result:
        print(f"✓ Found YouTube captions for video {video_id}")
        return result
    
    # Fall back to Whisper
    print(f"No YouTube captions found, using Whisper...")
    
    if audio_path is None:
        raise ValueError("Audio file required for Whisper transcription")
    
    return transcribe_with_whisper(audio_path)
