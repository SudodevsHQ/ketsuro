from typing import Text
from fireo.models import Model
from fireo.fields import TextField

class Video(Model):
    video_id = TextField()
    summary = TextField()
    summary_video = TextField()