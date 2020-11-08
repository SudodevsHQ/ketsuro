from typing import Text
from fireo.models import Model
from fireo.fields import TextField

class Video(Model):
    yt_url = TextField()
    summary = TextField()
    summary_video = TextField()