# ketsuro-backend
Submission for Hackout 2020

[Ketsuro Client](https://github.com/sudodevsHQ/ketsuro-client)

## Installation 
cd to `ketsuro/` and create a virtual environment
```
python -m venv env
```
activate the virtual environment
```
source env/bin/activate
```

then
```
pip install -r requirements.txt
```

debug
```
uvicorn main:app --reload
```

deploy
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
