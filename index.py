#!/home/vale/dev/python/progetto-gestione/python_venv/bin/python3
#from ysa.indexing.sentiment_analysis import SentimentAnalizer
#from ysa.indexing import VideoIndexer
from ysa.indexing import *

print("Starting indexing...")
sa = SentimentAnalyzer()
ix = VideoIndexer('indexdir', sa)
ix.write('data')
sa.write()
