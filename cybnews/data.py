import os
import string
import json
from collections import Counter
import pandas as pd

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer


MODEL_PATH = os.getenv("MODEL_PATH")
DATA_PATH = os.getenv("DATA_PATH")

LANGUAGE='english'
STOPWORDS_DEL = ["not", "no", "nor", "against", "however", "but", "never", "should", "would" , "could", "might", "must", "no", "yes", "always", "none", "only", "still", "yet", "despite", "unless", "until", "cannot" ]
STOPWORDS_ADD = ["reuters"]



def get_data(path):
    return pd.read_csv(path)


def tokenize(sentence):
    sentence = sentence.strip()
    sentence = sentence.lower()
    sentence = "".join(char for char in sentence if not char.isdigit())

    for x in string.punctuation:
        sentence = sentence.replace(x, '')

    for x in ['’', '“', '”', '—', '"' ]:
        sentence = sentence.replace(x, '')

    return word_tokenize(sentence)


def clear_stopwords(tokens, stopw_add=[], stopw_del=[], lang=LANGUAGE):
    stop_words = set(stopwords.words(lang))
    stop_words.update(stopw_add)
    stop_words.difference_update(stopw_del)

    return [w for w in tokens if w not in stop_words]


def preprocessing(sentence):
    tokens = tokenize(sentence)
    v_l = [WordNetLemmatizer().lemmatize(word, pos = "v") for word in tokens]
    lemmatized_token = [WordNetLemmatizer().lemmatize(word, pos = "n") for word in v_l]

    clean_tokens = clear_stopwords(
        lemmatized_token,
        stopw_del=STOPWORDS_DEL,
        stopw_add=STOPWORDS_ADD
    )


    return ' '.join(clean_tokens)


def preprocess_input(text: str):
    return [preprocessing(text)]



### WELF data set specific
#
def welf_join_text(data: pd.DataFrame):
    data = data.fillna('')
    data["all_text"] = data["title"] + " " +  data["text"]
    return data


def welf_preprocessing(data: pd.DataFrame):
    data["all_text_cleaned"] = data["all_text"].apply(preprocessing)
    return data[["all_text_cleaned", "label"]]


### ISOT data set specifiv
#
def isot_join_text(data: pd.DataFrame):
    """ISOT also has 'tilte' and 'text' columns..."""
    data["all_text"] = data["title"] + " " +  data["text"]
    return data


def isot_preprocessing(data: pd.DataFrame):
    data["all_text_cleaned"] = data["all_text"].apply(preprocessing)
    return data[["all_text_cleaned"]]

