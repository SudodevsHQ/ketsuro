from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import youtube_dl
import json

from utils import punctuate
from models.PunctuatedResponse import PunctuatedTranscript

app = FastAPI()

@app.get('/video/{video_id}')
def get_video(video_id: str):
    data = YouTubeTranscriptApi.get_transcript(video_id)
    raw_transcript = ' '
    raw_transcript = raw_transcript.join([f"{info['text']}" for info in data])
    response = punctuate(raw_transcript)
    response = json.loads(response.text)

    raw_text = '\n'
    raw_text = raw_text.join([f"{info['start']}: {info['text']}" for info in data])
    print(raw_text)

    ytdl_opts = {
        'outtmpl': f"videos/{response['request_id']}",
        'nooverwrites': True
    }
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([f'http://www.youtube.com/watch?v={video_id}'])

    return response

@app.post('/webhook')
def getPunctuate(item: PunctuatedTranscript):
    print(item)