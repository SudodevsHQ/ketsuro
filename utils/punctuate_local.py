from punctuator import Punctuator
# from tinydb import TinyDB, Query

# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
# from sumy.nlp.stemmers import Stemmer
# from sumy.utils import get_stop_words
# from utils.get_regions import get_regions

# from utils.clip import clip_video
# from utils.upload_summary import upload_summary, update_summarized_video



from utils.upload_summary import upload_summary



p = Punctuator('model-euro.pcl')
async def punctuate_locally(text):
    # db = TinyDB('db.json')    
    # Videos = Query()
    # video = db.fastsearch(Videos.video_id == video_id)[0]
    print('\n[INFO]: Loading model...\n')
    print('[SUCCESS]: Model loaded\n\n[INFO]: Punctuating\n')
    punctuatedCaptions = p.punctuate(text)
    
    return punctuatedCaptions

    # # print(punctuatedCaptions)
    # print('--------Punctuation Done----------\n POWERED BY AMD RYZEN 5900HS 🚀\n  ')
    # LANGUAGE = 'english'

    # # SENTENCE_COUNT = video['SENTENCE_COUNT'] if not video['SENTENCE_COUNT'] == None else int(
    # #     len(punctuatedCaptions.split('.'))*0.2)

    # SENTENCE_COUNT = 5 
    
    # parser = PlaintextParser.from_string(
    #     punctuatedCaptions, Tokenizer(LANGUAGE))
    # stemmer = Stemmer(LANGUAGE)
    # summarizer = Summarizer(stemmer)
    # summarizer.stop_words = get_stop_words(LANGUAGE)

    # summarized_text_list = []
    # for sentence in summarizer(parser.document, SENTENCE_COUNT):
    #     summarized_text_list.append(sentence._text)

    # return summarized_text_list
  

