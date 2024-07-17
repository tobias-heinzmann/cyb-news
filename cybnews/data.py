#!/usr/bin/env python3

import pandas as pd
import string

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer


def get_data(path):
    return pd.read_csv(path)


def join_text_welf(data: pd.DataFrame) -> pd.DataFrame:
    data = data.fillna('')
    data["all_text"] = data["title"] + " " +  data["text"]
    return data


def _preprocessing(sentence):
    sentence = sentence.strip()
    sentence = sentence.lower()
    sentence = "".join(char for char in sentence if not char.isdigit())
    
    for x in string.punctuation:
        sentence = sentence.replace(x, "")

    for x in ["’", "“", "”", "-" ]:
        sentence = sentence.replace(x, "")

    tokens = word_tokenize(sentence)

    language = set(stopwords.words("english"))
    #language.update(["trump", "clinton", "obama"])
    language.difference_update(["not", "no","nor", "against", "however", "but", "never", "should", "would" , "could", "might", "must", "no", "yes", "always", "none", "only", "still", "yet", "despite", "unless", "until", "cannot" ])
    sentence = [w for  w in tokens if not w in language]
    v_l = [WordNetLemmatizer().lemmatize(word, pos = "v") for word in sentence]
    n_l = [WordNetLemmatizer().lemmatize(word, pos = "n") for word in v_l]
    return ' '.join(n_l)


def preprocessing(data: pd.DataFrame) -> pd.DataFrame:
    data["all_text_cleaned"] = data["all_text"].apply(_preprocessing)
    data_preprocessed = data[["all_text_cleaned", "label"]]
    return data_preprocessed


def preprocess_input(text: str):
    return [_preprocessing(text)]
    