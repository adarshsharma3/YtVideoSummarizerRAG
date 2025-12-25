from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
ytt_api = YouTubeTranscriptApi()
def extract_video_id(url: str) -> str:
    query = urlparse(url).query
    return parse_qs(query)["v"][0]

def get_transcript(video_url: str) -> str:
    print("*******************")
    video_id = extract_video_id(video_url)
    transcript=ytt_api.fetch(video_id)
    
    print(transcript)
    return " ".join(chunk.text for chunk in transcript.snippets)
