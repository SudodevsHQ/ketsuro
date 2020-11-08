import fireo
from fireo.database import db
from main import app

from fastapi import Request


@app.middleware("http")
async def dispatch(request: Request, call_next):
    fireo.connection(
        from_file='ketsuro-69-firebase-adminsdk-aqsts-af77273ea3.json')
    request.state.fireo = fireo
    request.state.db = db
    response = await call_next(request)
    return response
