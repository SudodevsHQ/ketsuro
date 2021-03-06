from typing import Text
from fireo.models import Model
from fireo.fields import TextField, ListField

class Video(Model):
    video_id = TextField()
    summary = TextField()
    summary_video = TextField()
    request_id = TextField()
    punctuatedCaptions = ListField()