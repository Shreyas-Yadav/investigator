"""YouTube video utilities - extract video ID and download audio."""

import re
import os
import tempfile
from pathlib import Path
import yt_dlp


def extract_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from various URL formats.
    
    Supports:
    - youtube.com/watch?v=VIDEO_ID
    - youtu.be/VIDEO_ID
    - youtube.com/embed/VIDEO_ID
    - youtube.com/shorts/VIDEO_ID
    """
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/watch\?.*v=)([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def get_video_info(video_id: str) -> dict:
    """Get video metadata (title, duration, etc.)."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Unknown'),
            'duration': info.get('duration', 0),
            'channel': info.get('uploader', 'Unknown'),
            'thumbnail': info.get('thumbnail', ''),
        }


def download_audio(video_id: str, output_dir: str | None = None) -> str:
    """
    Download audio from YouTube video.
    
    Args:
        video_id: YouTube video ID
        output_dir: Directory to save the audio file (uses temp dir if None)
    
    Returns:
        Path to the downloaded audio file
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    
    output_path = os.path.join(output_dir, f"{video_id}.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Return the actual file path (with .mp3 extension)
    return os.path.join(output_dir, f"{video_id}.mp3")
