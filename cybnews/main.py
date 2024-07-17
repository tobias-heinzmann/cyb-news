from cybnews.data import get_data, join_text_welf, preprocessing
from cybnews.model import train_test_split_data, create_new_model, save_model, load_model

MODEL_PATH = ""
DATA_PATH = ""


if __name__ == "__main__":
    data = get_data(DATA_PATH)
    data = join_text_welf(data)
    # data = data.sample(frac=0.1, random_state=42)
    data = preprocessing(data)
    X_train, X_test, y_train, y_test  = train_test_split_data(data)
    model = create_new_model(X_train, y_train)
    save_model(model, MODEL_PATH)

