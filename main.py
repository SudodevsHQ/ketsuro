from os import error
from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from tinydb import TinyDB, Query
import youtube_dl
import json
import os

from utils import punctuate
from models.PunctuatedResponse import PunctuatedTranscript

app = FastAPI()

@app.get('/video/{video_id}')
def get_video(video_id: str):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id)
        raw_transcript = ' '
        raw_transcript = raw_transcript.join([f"{info['text']}" for info in data])


        raw_text = '\n'
        raw_text = raw_text.join([f"{info['start']}: {info['text']}" for info in data])
        print(raw_text)

        # download the video with video_id as the name
        ytdl_opts = {
            'outtmpl': f"videos/{video_id}",
            'nooverwrites': True
        }
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            ydl.download([f'http://www.youtube.com/watch?v={video_id}'])

        response = punctuate(raw_transcript)
        response = json.loads(response.text)
        
        # map request id to video id
        db = TinyDB('db.json')
        db.insert({'request_id': response['request_id'], 'video_id': video_id})
        return response
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'code': 'TRANSCRIPT_NOT_FOUND', 'message': 'The transcript could not be found for the video'})
        

@app.post('/webhook')
def getPunctuate(item: PunctuatedTranscript):
    db = TinyDB('db.json')
    Videos = Query()
    video = db.search(Videos.request_id == item.request_id)[0]

    os.remove(os.path.join('videos',f"{video['video_id']}.mkv"))
    print(item.response)