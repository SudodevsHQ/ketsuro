from fastapi import APIRouter, HTTPException
from tinydb import TinyDB, Query
import os

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from models.PunctuatedResponse import PunctuatedTranscript

router = APIRouter()

@router.post('/webhook')
def punctuateAndSnip(punctuatedResponse: PunctuatedTranscript):
    db = TinyDB('db.json')
    Videos = Query()
    video = db.search(Videos.request_id == punctuatedResponse.request_id)[0]

    punctuatedCaptions = punctuatedResponse.response['punctuated_texts'][0]

    LANGUAGE = 'english'
    parser = PlaintextParser.from_string(punctuatedCaptions, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, 5):
        print(sentence)

    # os.remove(os.path.join('videos',f"{video['video_id']}.mkv"))
    # print(punctuatedResponse.response)