import pandas as pd
import string

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

from collections import Counter
import json
LANGUAGE='english'
STOPWORDS_DEL = ["not", "no", "nor", "against", "however", "but", "never", "should", "would" , "could", "might", "must", "no", "yes", "always", "none", "only", "still", "yet", "despite", "unless", "until", "cannot" ]
STOPWORDS_ADD = ["reuters"]
MODEL_PATH = "/Users/admin/code/frederiklm/cyb-news/models"
DATA_PATH = "/Users/admin/code/frederiklm/cyb-news/data/WELFake_Dataset.csv"

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





# Build Dict for Wordcloud



def get_word_count(sentence):
    tokens = tokenize(sentence)
    v_l = [WordNetLemmatizer().lemmatize(word, pos = "v") for word in tokens]
    lemmatized_token = [WordNetLemmatizer().lemmatize(word, pos = "n") for word in v_l]
    clean_tokens = clear_stopwords(
        lemmatized_token,
        stopw_del=STOPWORDS_DEL,
        stopw_add=STOPWORDS_ADD
    )
    word_counts = Counter(clean_tokens)
    return word_counts


def get_word_cloud(data: pd.DataFrame):
    data = welf_join_text(data)
    data["counted"] = data["all_text"].apply(get_word_count)
    real_news= data[data["label"] == 0]
    fake_news= data[data["label"] == 1]
    total_word_counts_fake = Counter()

    for counts in fake_news["counted"]:
        total_word_counts_fake.update(counts)
    total_fake = sum(total_word_counts_fake.values())

    total_word_counts_real = Counter()
    for counts in real_news["counted"]:
        total_word_counts_real.update(counts)
    total_real = sum(total_word_counts_real.values())

    relative_freq_fake = {word: count / total_fake for word, count in total_word_counts_fake.items()}
    relative_freq_real = {word: count / total_real for word, count in total_word_counts_real.items()}

    all_words = set(relative_freq_fake.keys()).union(set(relative_freq_real.keys()))
    diffs = {word: relative_freq_fake.get(word, 0) - relative_freq_real.get(word, 0) for word in all_words}

    fake_uptop = dict(sorted(diffs.items(), key=lambda item: item[1], reverse=True))
    fake_uptop_list = list(fake_uptop.items())
    fake_uptop_list_200 = fake_uptop_list[:200]
    words_overrepresented_in_fakes = dict(fake_uptop_list_200)

    fake_uptop_revesed = {word: -value for word, value in fake_uptop.items()}
    real_uptop= dict(sorted(fake_uptop_revesed.items(), key=lambda item: item[1], reverse=True))
    real_uptop_list = list(real_uptop.items())
    real_uptop_list_200 = real_uptop_list[:200]
    words_overrepresented_in_real = dict(real_uptop_list_200)
    print(words_overrepresented_in_real)

    return words_overrepresented_in_real, words_overrepresented_in_fakes # dict


def save_wordcloud(dict_real, dict_fake, model_path=MODEL_PATH):
    with open(f'{model_path}/words_real.json', 'w') as json_file:
        json.dump(dict_real, json_file)
    with open(f'{model_path}/words_fake.json', 'w') as json_file:
        json.dump(dict_fake, json_file)





if __name__ == '__main__':
    data = get_data(DATA_PATH)
    data= welf_join_text(data)
    real, fake = get_word_cloud(data)
    save_wordcloud(real,fake, MODEL_PATH)
