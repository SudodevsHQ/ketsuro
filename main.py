from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi

from utils import punctuate
from models.PunctuatedResponse import PunctuatedTranscript

app = FastAPI()

@app.get('/video/{video_id}')
def get_video(video_id: str):
    data = YouTubeTranscriptApi.get_transcript(video_id)
    raw_transcript = ' '
    raw_transcript = raw_transcript.join([f"{info['text']}" for info in data])

    response = punctuate(raw_transcript)
    return response.text

@app.post('/webhook')
def getPunctuate(item: PunctuatedTranscript):
    print(item)