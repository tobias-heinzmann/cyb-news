import random
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware


MAX_REQ_TEXT=10000
app = FastAPI()
# app.state.model = load_model()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def root():
    return {
        'message': "This is the CYB News API. Be welcome."
    }

@app.get("/predict")
def get_predict(text: Annotated[str, Query(max_length=MAX_REQ_TEXT)]):
    return _response_predict(text)


@app.post("/predict")
def post_predict(text: Annotated[str, Query(max_length=MAX_REQ_TEXT)]):
    return _response_predict(text)


@app.put("/predict")
def put_predict(text: Annotated[str, Query(max_length=MAX_REQ_TEXT)]):
    return _response_predict(text)


def _response_predict(text: str):
    return {
        'fake': _predict_class(text),
        'probability': _predict_proba(text)
    }


def _predict_class(text: str):
    return bool(random.getrandbits(1))
    

def _predict_proba(text: str):
    return random.uniform(-1, 1)
