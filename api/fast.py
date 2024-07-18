import random
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from cybnews.model import load_model
from cybnews.data import preprocess_input, load_wordcloud

import os

WORDCLOUD_FAKE_PATH = os.getenv("WORDCLOUD_FAKE_PATH")
WORDCLOUD_REAL_PATH = os.getenv("WORDCLOUD_REAL_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")


MAX_REQ_TEXT=15000
app = FastAPI()
app.state.model = load_model(MODEL_PATH)


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


def _response_predict(text: str):
    y_pred = app.state.model.predict(preprocess_input(text))
    return {
        'fake': bool(y_pred[0]),
        'probability': _predict_proba(text)
    }


def _predict_proba(text: str):
    return random.uniform(-1, 1)

""""""

real_words_file = load_wordcloud(WORDCLOUD_REAL_PATH)
fake_words_file = load_wordcloud(WORDCLOUD_FAKE_PATH)

@app.get("/wordcloud_fake")
def get_wordclouds():
    return fake_words_file



@app.get("/wordcloud_real")
def get_wordclouds():
    return real_words_file
