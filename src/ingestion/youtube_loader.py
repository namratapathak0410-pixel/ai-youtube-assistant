# src/ingestion/youtube_loader.py

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound
)
from langchain_core.documents import Document


def load_video(url):
    video_id = url.split("v=")[-1]

    try:
        # Try default transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

    except NoTranscriptFound:
        try:
            # Try English manually
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=['en']
            )
        except Exception:
            return [Document(page_content="❌ No transcript available")]

    except TranscriptsDisabled:
        return [Document(page_content="❌ Transcripts are disabled")]

    except Exception as e:
        return [Document(page_content=f"❌ Error: {str(e)}")]

    # Convert to text
    text = " ".join([t['text'] for t in transcript])

    return [Document(page_content=text)]