from cybnews.data import get_data, welf_join_text, preprocessing, preprocess_input, welf_preprocessing
from cybnews.model import train_test_split_data, create_new_model, save_model, load_model

MODEL_PATH = "/Users/admin/code/frederiklm/cyb-news/models"
DATA_PATH = "/Users/admin/code/frederiklm/cyb-news/data/WELFake_Dataset.csv"


if __name__ == "__main__":
    data = get_data(DATA_PATH)
    data = welf_join_text(data)
    #data = data.sample(frac=0.01, random_state=42)
    data = welf_preprocessing(data)
    X_train, X_test, y_train, y_test  = train_test_split_data(data)
    model = create_new_model(X_train, y_train)
    #model = load_model('model.pkl', MODEL_PATH)
    save_model(model, MODEL_PATH)
    pred = model.predict(preprocess_input('sadfasdfs v dfgesgxwe'))
    pred_proba = model.predict_proba(preprocess_input('sadfasdfs v dfgesgxwe'))

    print(pred)
    print(pred_proba)
