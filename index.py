#!/home/vale/dev/python/progetto-gestione/python_venv/bin/python3
from indexing.sentiment_analysis import SentimentAnalizer
from indexing.whoosh_indexing import VideoIndexer

print("Starting indexing...")
sa = SentimentAnalizer()
ix = VideoIndexer('indexdir', sa)
ix.write('data')
sa.write()
