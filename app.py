from flask import Flask, render_template, request
from youtube_transcript import fetch_transcript
from summarizer import TextSummarizer
from db_manager import DatabaseManager

app = Flask(__name__)

# Azure Cognitive Services API credentials
ENDPOINT = "//vidbreeze.cognitiveservices.azure.com/"
KEY = "521895e58968414eb2b895b7c7e7c3fa"

# Database credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "saloni"
DB_NAME = "youtubetranscript"

text_summarizer = TextSummarizer(ENDPOINT, KEY)
db_manager = DatabaseManager(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        video_id = video_url.split('v=')[-1]

        # Check if transcript already exists in the database
        transcript = db_manager.fetch_transcript(video_url)
        if transcript:
            print(f"Transcript fetched from database: {transcript}")
            return render_template('result.html', transcript=transcript)  # Render the transcript

        # If no transcript is found, fetch it from YouTube
        transcript = fetch_transcript(video_id)
        if transcript:
            print(f"Transcript fetched successfully: {transcript}")
        else:
            print(f"Transcript not available for video ID: {video_id}")
            return "Transcript not available."

        # Try summarizing the transcript
        try:
            summary = text_summarizer.summarize(transcript)
            print(f"Summary generated: {summary}")
        except Exception as e:
            print(f"Error summarizing transcript: {e}")
            return "Error summarizing the transcript."

        # Save the transcript and summary to the database
        db_manager.insert_summary(video_url, transcript, summary)
        print(f"Summary saved to database for video: {video_url}")
        return render_template('result.html', transcript=transcript, summary=summary)  # Pass both transcript and summary if needed

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
