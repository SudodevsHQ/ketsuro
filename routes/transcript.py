from typing import Optional
from fastapi import APIRouter, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import json

from utils.punctuate import punctuate
from tinydb import TinyDB
from utils.punctuate_local import punctuate_locally

router = APIRouter()

@router.get('/video/{video_id}')
async def generate_transcript(video_id: str, SENTENCE_COUNT: Optional[int] = None):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id)
        raw_transcript = ' '
        raw_transcript = raw_transcript.join([f"{info['text']}" for info in data])

        response = await punctuate(raw_transcript)
        response = json.loads(response.text)
        punctuate_locally(raw_transcript, response['request_id'])
        
        db = TinyDB('db.json')
        db.insert({'request_id': response['request_id'], 'video_id': video_id, 'SENTENCE_COUNT': SENTENCE_COUNT, 'transcript': data})
        return response
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'code': 'TRANSCRIPT_NOT_FOUND', 'message': 'The transcript could not be found for the video'})
        
