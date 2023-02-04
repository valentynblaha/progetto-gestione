from indexing.sentiment_analysis import SentimentAnalizer
from indexing.whoosh_indexing import VideoIndexer

ix = VideoIndexer('indexdir', SentimentAnalizer())
ix.write('data')
