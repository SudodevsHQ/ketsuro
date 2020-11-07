from fastapi import FastAPI, HTTPException

from routes import transcript, punctuate_and_snip

app = FastAPI()

app.include_router(transcript.router)
app.include_router(punctuate_and_snip.router)