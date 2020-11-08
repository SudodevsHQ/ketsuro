from pydantic import BaseModel

class PunctuatedTranscript(BaseModel):
    request_id: str
    response: dict
