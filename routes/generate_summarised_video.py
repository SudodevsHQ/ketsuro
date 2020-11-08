from fastapi import APIRouter, HTTPException
from typing import Optional
import youtube_dl
from tinydb import TinyDB, Query

from utils.get_regions import get_regions
from utils.clip import clip_video
from utils.file_upload import upload_file
from utils.upload_summary import update_summarized_video
from utils.upload_summary import upload_summary
from models.video_model import Video

router = APIRouter()


@router.get('/summarize/{video_id}')
async def generateVideo(video_id: str, request_id: str, SENTENCE_COUNT: Optional[int] = None):
    try:
        ytdl_opts = {
            'outtmpl': f"videos/{video_id}",
            'nooverwrites': True,
            'format': '18'
        }
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            ydl.download([f'http://www.youtube.com/watch?v={video_id}'])
            
        db = TinyDB('db.json')
        Videos = Query()
        
        transcript = db.search(Videos.request_id == request_id)[0]['transcript']
        video = Video.collection.filter('video_id', '==', video_id).get()
        summarized_text_list = video.summary.split('.')
        
        SENTENCE_COUNT = SENTENCE_COUNT if not SENTENCE_COUNT == None else int(len(summarized_text_list)*0.2)

        regions = get_regions(summarized_text_list, transcript, SENTENCE_COUNT)
        await clip_video(video_id, regions)
        uploaded_url = await upload_file(f"clipped/{video_id}.mp4")
        await update_summarized_video(video_id, uploaded_url)

        # os.remove(os.path.join('videos',f"{video['video_id']}"))        
        return True
    
    except Exception as e:
        print(e)
        upload_summary(video_id, 'TRANSCRIPT_NOT_FOUND')    
        raise HTTPException(status_code=500, detail={'code': 'VIDEO_ERROR', 'message': 'There was an error generating the video'})
        
