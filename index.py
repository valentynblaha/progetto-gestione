from indexing.sentiment_analysis import SentimentAnalizer
from indexing.whoosh_indexing import VideoIndexer

sa = SentimentAnalizer()
ix = VideoIndexer('indexdir', sa)
ix.write('data')
sa.write()
