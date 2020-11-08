from fastapi import APIRouter
from tinydb import TinyDB, Query

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from models.PunctuatedResponse import PunctuatedTranscript
from utils.upload_summary import upload_summary

router = APIRouter()


@router.post('/webhook')
async def punctuateAndSummarise(punctuatedResponse: PunctuatedTranscript):
    db = TinyDB('db.json')
    Videos = Query()
    video = db.search(Videos.request_id == punctuatedResponse.request_id)[0]

    punctuatedCaptions = punctuatedResponse.response['punctuated_texts'][0]

    LANGUAGE = 'english'

    SENTENCE_COUNT = video['SENTENCE_COUNT'] if not video['SENTENCE_COUNT'] == None else int(
        len(punctuatedCaptions.split('.'))*0.2)

    parser = PlaintextParser.from_string(
        punctuatedCaptions, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summarized_text_list = []
    for sentence in summarizer(parser.document, SENTENCE_COUNT):
        summarized_text_list.append(sentence._text)

    await upload_summary(video['video_id'], ' '.join(summarized_text_list), punctuatedCaptions.split('.'), video['request_id'])    

