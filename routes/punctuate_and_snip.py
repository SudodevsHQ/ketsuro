from fastapi import APIRouter
from tinydb import TinyDB, Query

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from models.PunctuatedResponse import PunctuatedTranscript
from utils.get_regions import get_regions
from utils.clip import clip_video
from utils.file_upload import upload_file

router = APIRouter()


@router.post('/webhook')
def punctuateAndSnip(punctuatedResponse: PunctuatedTranscript):
    db = TinyDB('db.json')
    Videos = Query()
    video = db.search(Videos.request_id == punctuatedResponse.request_id)[0]

    punctuatedCaptions = punctuatedResponse.response['punctuated_texts'][0]

    LANGUAGE = 'english'

    SENTENCE_COUNT = video['SENTENCE_COUNT'] if not video['SENTENCE_COUNT'] == None else int(
        len(punctuatedCaptions.split('.'))*0.2)
    print(SENTENCE_COUNT, len(punctuatedCaptions.split('.')))
    parser = PlaintextParser.from_string(
        punctuatedCaptions, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summarized_text_list = []
    for sentence in summarizer(parser.document, SENTENCE_COUNT):
        summarized_text_list.append(sentence._text)

    # TODO: update firestore with sumarized_text_list
    regions = get_regions(summarized_text_list,
                          video['transcript'], SENTENCE_COUNT)
    clip_video(video['video_id'], regions)

    uploaded_url = upload_file(f"clipped/{video['video_id']}.mp4")


    # os.remove(os.path.join('videos',f"{video['video_id']}"))
