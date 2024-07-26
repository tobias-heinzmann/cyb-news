import os
import json
from collections import Counter
import pandas as pd

from nltk.stem import WordNetLemmatizer

from .data import get_data, join_text, clear_stopwords, tokenize, STOPWORDS_DEL, STOPWORDS_ADD, DATA_PATH

WORDCLOUD_FAKE_PATH = os.getenv("WORDCLOUD_FAKE_PATH")
WORDCLOUD_REAL_PATH = os.getenv("WORDCLOUD_REAL_PATH")



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
    data = join_text(data)
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

    return words_overrepresented_in_real, words_overrepresented_in_fakes # dict


def save_wordcloud(dict_to_store,json_path):
    with open(json_path, 'w') as json_file:
        json.dump(dict_to_store, json_file)


def load_wordcloud(file_name):
    if file_name is None:
        return {}

    with open(file_name, 'r') as j_name:
        dict_words = json.load(j_name)
    return dict_words


def generate_wordclouds_welf(control_print=True):
    data = get_data(DATA_PATH)
    real, fake = get_word_cloud(welf_join_text(data))
    save_wordcloud(real, WORDCLOUD_REAL_PATH)
    save_wordcloud(fake, WORDCLOUD_FAKE_PATH)

    if not control_print:
        return

    words_fake = load_wordcloud(WORDCLOUD_FAKE_PATH)
    words_real = load_wordcloud(WORDCLOUD_REAL_PATH)

    print('words fake:')
    print(words_fake)
    print()
    print('words real:')
    print(words_real)


if __name__ == '__main__':
    generate_wordclouds_welf()
