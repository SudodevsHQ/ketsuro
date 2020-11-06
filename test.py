
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from youtube_transcript_api import YouTubeTranscriptApi

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 120
vid_id = '8gNTyr1DXc4'

data = YouTubeTranscriptApi.get_transcript(vid_id)

raw_text = ' '
raw_text.join([info['text'] for info in data])


if __name__ == "__main__":

    parser = PlaintextParser.from_string(raw_text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    print(parser.document)
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
