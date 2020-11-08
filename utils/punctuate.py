import requests
from environs import Env

env = Env()
env.read_env()

base_url = "https://proxy.api.deepaffects.com/text/generic/api/v1/async/punctuate"

def punctuate(text: str):
    querystring= {
        "apikey": env.str('DEEPAFFECTS_API_KEY'),
        "webhook": "http://621e47ca71ab.ngrok.io/webhook"
    }

    payload = {
            "texts": [text]
    }
    headers = {
        'Content-Type': "application/json",
    }
    response = requests.post(base_url, json=payload, headers=headers, params=querystring)
    return response
