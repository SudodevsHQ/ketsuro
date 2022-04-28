from fastapi import APIRouter, HTTPException
from typing import Optional
from youtube_dlp import YoutubeDL
from tinydb import TinyDB, Query

from utils.get_regions import get_regions
from utils.clip import clip_video
# from utils.file_upload import upload_file
from utils.upload_summary import update_summarized_video
from utils.upload_summary import upload_summary
from models.video_model import Video
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from utils.get_regions import get_regions
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer


from tinydb import TinyDB, Query

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

router = APIRouter()


@router.get('/summarize/{video_id}')
async def generateVideo(video_id: str, SENTENCE_COUNT: Optional[int] = None):
    try:
        ytdl_opts = {
            'outtmpl': f"videos/{video_id}",
            'nooverwrites': True,
            'format': '18'
        }
        
        print('[INFO]----DOWNLOAD STARTED------\n')
        
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            ydl.download([f'http://www.youtube.com/watch?v={video_id}'])
            
        print('[INFO]----DOWNLOAD COMPLETE------\n')
        
            
        db = TinyDB('db.json')
        Videos = Query()
        
        
        
        transcript = db.search(Videos.video_id == video_id)[0]['transcript']
        print('----TRANSCRIPT FOUND------\n')
        
        
        punctuated_captions = db.search(Videos.video_id == video_id)[0]['punctuated_captions']
        
        print('----SUMMARIZATION STARTED------\n')
        
                
        LANGUAGE = 'english'
         
        parser = PlaintextParser.from_string(
            punctuated_captions, Tokenizer(LANGUAGE))
        
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        summarized_text_list = []
        for sentence in summarizer(parser.document, SENTENCE_COUNT if SENTENCE_COUNT else len(punctuated_captions.split('.'))*0.2):
            summarized_text_list.append(sentence._text)
            
            
        print('[SUCCESS]----SUMMARIZATION DONE------\n')
        

            
        # video = Video.collection.filter('video_id', '==', video_id).get()
        # summarized_text_list = video.summary.split('.')
        
        
        
        SENTENCE_COUNT = SENTENCE_COUNT if not SENTENCE_COUNT == None else int(len(punctuated_captions.split('.'))*0.2)

        regions = get_regions(summarized_text_list, transcript, SENTENCE_COUNT)
        
        
        await clip_video(video_id, regions)
        
        print('----VIDEO CLIPPED------\n')
        # uploaded_url = await upload_file(f"clipped/{video_id}.mp4")
        await update_summarized_video(video_id, 'ok')

        # os.remove(os.path.join('videos',f"{video['video_id']}"))        
        return True
    
    except Exception as e:
        print(e)
        # upload_summary(video_id, 'TRANSCRIPT_NOT_FOUND')    
        raise HTTPException(status_code=500, detail={'code': 'VIDEO_ERROR', 'message': 'There was an error generating the video'})
        
