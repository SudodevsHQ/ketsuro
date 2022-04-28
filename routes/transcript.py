from typing import Optional
from fastapi import APIRouter, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import json
from uuid import uuid4

from utils.punctuate import punctuate
from tinydb import TinyDB
from utils.punctuate_local import punctuate_locally
from utils.upload_summary import upload_summary

from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer


router = APIRouter()

@router.get('/video/{video_id}')
async def generate_transcript(video_id: str, SENTENCE_COUNT: Optional[int] = None):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id)
        raw_transcript = ' '
        raw_transcript = raw_transcript.join([f"{info['text']}" for info in data])
    
        request_id = str(uuid4())
        response = { 'request_id': request_id, 'video_id': video_id, 'SENTENCE_COUNT': SENTENCE_COUNT, 'transcript': data,  }

        db = TinyDB('db.json')
        db.insert(response)
        punctuate_and_summarize_and_upload(raw_transcript, SENTENCE_COUNT, request_id, video_id)
        return response
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={'code': 'TRANSCRIPT_NOT_FOUND', 'message': 'The transcript could not be found for the video'})
        


async def punctuate_and_summarize_and_upload(raw_transcript, SENTENCE_COUNT, request_id, video_id): 
        punctuated_captions = await punctuate_locally(raw_transcript)
    
        
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
        
        print('--------FIRBABLE upload STARTED--------\n')
        await upload_summary(video_id, ' '.join(summarized_text_list), request_id)    
        print('--------FIRBABLE upload END--------\n')
        