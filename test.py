
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
SENTENCES_COUNT = 4
# vid_id = '5tQLFon8Yhk'

# data = YouTubeTranscriptApi.get_transcript(vid_id)

# raw_text = ' '
# raw_text = raw_text.join([f"{info['start']}: {info['text']}" for info in data])
# print(raw_text)

if __name__ == "__main__":

    parser = PlaintextParser.from_string('''Oh, no, a the it's not, it's it. There's no need even to have a college degree at all. We're in high school, but I mean, if somebody graduated from a great university that maybe in indeed, that may be an indication that they will be capable of great things, but it's not necessarily the case. You know, if you look at say people like Bill Gates or Larry Ellison, Steve Jobs.  These guys didn't graduate from college, but if you had a chance to hire them.  Of course, that would be a good idea, so you know, just looking just for evidence of exceptional ability, and if there's a track record of exceptional achievement, then it's likely that that will continue into the future.''', Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    print(parser.document)
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
