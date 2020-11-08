from fastapi import FastAPI, HTTPException, Request
import fireo
from fireo.database import db

from routes import transcript, punctuate_and_summarise, generate_summarised_video

app = FastAPI()


@app.middleware("http")
async def dispatch(request: Request, call_next):
    fireo.connection(
        from_file='ketsuro-69-firebase-adminsdk-aqsts-af77273ea3.json')
    request.state.fireo = fireo
    request.state.db = db
    response = await call_next(request)
    return response


app.include_router(transcript.router)
app.include_router(punctuate_and_summarise.router)
app.include_router(generate_summarised_video.router)
