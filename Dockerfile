#FROM tensorflow/tensorflow:2.17.0
FROM python:3.10.6

COPY cybnews cybnews
COPY setup.py setup.py
COPY api api
COPY requirements.txt requirements.txt
COPY models models
COPY wordcloud wordcloud
RUN mkdir -p /data

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt stopwords wordnet
RUN pip install .

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
