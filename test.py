
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from punctuator import Punctuator
from youtube_transcript_api import YouTubeTranscriptApi

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import os

LANGUAGE = "english"
SENTENCES_COUNT = 5
vid_id = '8gNTyr1DXc4'


data = YouTubeTranscriptApi.get_transcript(vid_id)
raw_text = ' '.join([info['text'] for info in data])

p = Punctuator('models/INTERSPEECH-T-BRNN.pcl')
punc_text = p.punctuate(raw_text)


print('-------------------------------------\n')

if __name__ == "__main__":

    parser = PlaintextParser.from_string(punc_text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
