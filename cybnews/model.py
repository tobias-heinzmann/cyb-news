from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import joblib


MODEL_PATH = "/models"
MODEL_NAME = 'model_2.pkl'


def train_test_split_data(data: pd.DataFrame):
    """
    """
    X_train, X_test, y_train, y_test = train_test_split(
        data["all_text_cleaned"],
        data["label"],
        test_size=0.3,
        random_state=42
        )
    return X_train, X_test, y_train, y_test


def create_new_model(X_train, y_train):
    """
    Creates a new model
    """
    pipeline = make_pipeline(
        TfidfVectorizer(
            ngram_range = (1, 2)),
            SVC(
                C = 10,
                degree = 1,
                kernel = 'sigmoid'
            )
        )
    pipeline.fit(X_train, y_train)

    return pipeline


def save_model(model, model_path=MODEL_PATH):
    """
    Stores the model in the model_path
    """
    joblib.dump(model, f"{model_path}model.pkl")


def load_model(model_name=MODEL_NAME, model_path=MODEL_PATH):
    """
    Retrieves the model from model_path
    """
    return joblib.load(f"{model_path}/{model_name}")
