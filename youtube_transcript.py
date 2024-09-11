from youtube_transcript_api import YouTubeTranscriptApi

def fetch_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None