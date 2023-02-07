from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whoosh.query
import whoosh.scoring
import os, os.path


class VideoSearcher():

    def __init__(self, indexdir) -> None:
        self.__ix = open_dir(indexdir)
        self.__searcher = self.__ix.searcher(weighting=whoosh.scoring.BM25F(B=0.75, K1=2))


    def parse_query(self, query_text):
        parser = QueryParser("content", schema=self.__ix.schema)
        all_parents = whoosh.query.Term("kind", "video")

        query = parser.parse(query_text)
        return query

    def search(self, query):
        return self.__searcher.search(query)

    def __del__(self):
        if self.__searcher is not None:
            self.__searcher.close()