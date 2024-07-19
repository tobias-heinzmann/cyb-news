import os
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from cybnews.model import load_model
from cybnews.data import preprocess_input
from cybnews.wordcloud import load_wordcloud


WORDCLOUD_FAKE_PATH = os.getenv("WORDCLOUD_FAKE_PATH")
WORDCLOUD_REAL_PATH = os.getenv("WORDCLOUD_REAL_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")
MAX_REQ_TEXT=15000

app = FastAPI()
app.state.model = load_model(MODEL_PATH)
app.state.real_words_file = load_wordcloud(WORDCLOUD_REAL_PATH)
app.state.fake_words_file = load_wordcloud(WORDCLOUD_FAKE_PATH)


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
    #      0           1
    # [[0.05986795 0.94013205]]
    
    print('performing predict')
    
    y_pred_proba = app.state.model.predict_proba(preprocess_input(text))
    
    print('predict done')
    
    fake = None
    proba = None    
    if y_pred_proba[0][0] > y_pred_proba[0][1]:
        fake = False
        proba = y_pred_proba[0][0]
    else:
        fake = True
        proba = y_pred_proba[0][1]

    return {
        'fake': fake,
        'probability': proba
    }


@app.get("/wordcloud_fake")
def get_wordclouds_fake():
    return app.state.fake_words_file


@app.get("/wordcloud_real")
def get_wordclouds_real():
    return app.state.real_words_file
