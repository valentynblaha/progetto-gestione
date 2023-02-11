"""
Package for searching and indexing the corpus of documents scraped from YouTube
"""
__all__ = ['VideoIndexer', 'VideoSearcher', 'SentimentAnalyzer']


from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser, dateparse
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from .utils import Singleton

import hashlib
import json
import os
import os.path
import dateutil.parser
import numpy
import pickle
import whoosh.query
import whoosh.scoring

class VideoIndexer():

    __ix = None
    __schema = Schema(id=STORED,
                videoId=STORED,
                kind=ID(stored=True),
                publishedAt=DATETIME,
                title=TEXT(field_boost=2, analyzer=analysis.StemmingAnalyzer()),
                user=ID(stored=True),
                likes=NUMERIC(int, stored=True),
                content=TEXT(phrase=True, analyzer=analysis.StemmingAnalyzer()),
                positive=NUMERIC(float, stored=True),
                neutral=NUMERIC(float, stored=True),
                negative=NUMERIC(float, stored=True))

    __sentiment_analyzer = None

    def __init__(self, indexdir, sentiment_analyzer=None) -> None:
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
        self.__ix = create_in(indexdir, self.__schema)
        if sentiment_analyzer is not None:
            self.__sentiment_analyzer = sentiment_analyzer

    
    def add_comment(self, writer, comment, videoId):
        text = comment['text']
        if self.__sentiment_analyzer is not None:
            scores = self.__sentiment_analyzer.get_score(text)
        else:
            scores = [0,0,0]
        writer.add_document(id=comment['id'],
                        videoId=videoId,
                        kind='comment',
                        publishedAt=dateutil.parser.isoparse(comment['publishedAt']),
                        user=comment['author'],
                        likes=comment['likes'],
                        content=text,
                        negative=scores[0],
                        neutral=scores[1],
                        positive=scores[2])
        return scores

    def index_video(self, writer, path):
    
        with open(path, 'r') as f:
            video = json.loads(f.read())
        L = 0
        video_scores = numpy.zeros(3)
        video_id = video['video']['id']
        for comment in video['comments']:
            scores = self.add_comment(writer, comment['topLevelComment'], video_id)
            weight = comment['topLevelComment']['likes'] + 1
            video_scores += numpy.array(scores) * weight
            L += weight
            if replies := comment.get('replies'):
                for reply in replies:
                    self.add_comment(writer, reply, video_id)
        video_scores /= L
        writer.add_document(kind='video',
                        id=video_id,
                        publishedAt=dateutil.parser.isoparse(video['video']['publishedAt']),
                        title=video['video']['title'],
                        likes=video['video']['likes'],
                        content=video['video']['description'],
                        negative=video_scores[0],
                        neutral=video_scores[1],
                        positive=video_scores[2]
                        )

    def write(self, data_dir, max_files=float('inf')):
        if self.__ix is not None:
            with self.__ix.writer() as w:
                filelist = os.listdir(data_dir)
                for i, filename in enumerate(filelist):
                    filepath = os.path.join(data_dir, filename)
                    print(f'Indexing file ({i}/{len(filelist)}): {filename} - {os.path.getsize(filepath)} bytes')
                    # For debugging
                    if (i >= max_files):
                       break
                    with w.group():
                        self.index_video(w, filepath)
                print("Writing the index...")


class VideoSearcher():

    __parser = None

    def __init__(self, indexdir) -> None:
        self.__ix = open_dir(indexdir)
        self.__searcher = self.__ix.searcher(weighting=whoosh.scoring.BM25F(B=0.75, K1=2))
        #self.__searcher = self.__ix.searcher(weighting=whoosh.scoring.TF_IDF())


    def parse_query(self, query_text):
        if self.__parser is None:
            self.__parser = MultifieldParser(["title","content"], schema=self.__ix.schema)
            self.__parser.add_plugin(dateparse.DateParserPlugin())

        query = self.__parser.parse(query_text)
        return query


    def search(self, query):
        return self.__searcher.search(query, limit=40)


    def __del__(self):
        if self.__searcher is not None:
            self.__searcher.close()


class SentimentAnalyzer(metaclass=Singleton):


    __roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    __model = AutoModelForSequenceClassification.from_pretrained(__roberta)
    __tokenizer = AutoTokenizer.from_pretrained(__roberta)
    __cache_filename = 'cache/sentiment_analysis.cache'
    __cache_dict = {}
    __cache_file = None

    def __init__(self) -> None:
        if not os.path.exists('cache'):
            os.mkdir('cache')
        if os.path.exists(self.__cache_filename):
            with open(self.__cache_filename, 'rb') as f:
                try:
                    self.__cache_dict = pickle.loads(f.read())
                except:
                    pass

    def score_text(self, text):
        encoded_text = self.__tokenizer(text, return_tensors='pt')
        try:
            output = self.__model(**encoded_text)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores).tolist()
        except:
            # Assign neutral score if scoring fails for some reasons
            scores = [0,1,0]
        return scores

    def write(self):
        if self.__cache_file is None:
            self.__cache_file = open(self.__cache_filename, 'wb')
        print("Writing sentiment analysis cache...")
        self.__cache_file.write(pickle.dumps(self.__cache_dict))
        self.__cache_file.close()

    def get_score(self, text):
        hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        score = self.__cache_dict.get(hash)
        if score is None:
            score = self.score_text(text)
            self.__cache_dict[hash] = score
        return score
