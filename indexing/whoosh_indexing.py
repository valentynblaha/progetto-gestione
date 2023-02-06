from whoosh.index import create_in
from whoosh.fields import *
import json
import os
import dateutil.parser
import numpy

class VideoIndexer():

    __ix = None
    __schema = Schema(id=STORED,
                kind=ID,
                publishedAt=DATETIME,
                title=TEXT(field_boost=2, analyzer=analysis.StemmingAnalyzer()),
                user=ID(stored=True),
                likes=NUMERIC(int, stored=True),
                content=TEXT(phrase=True, analyzer=analysis.StemmingAnalyzer()),
                positive=NUMERIC(float, stored=True),
                neutral=NUMERIC(float, stored=True),
                negative=NUMERIC(float, stored=True))

    __sentiment_analyzer = None

    def __init__(self, indexdir, sentiment_analyzer) -> None:
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
        self.__ix = create_in(indexdir, self.__schema)
        self.__sentiment_analyzer = sentiment_analyzer

    
    def add_comment(self, writer, comment):
        text = comment['text']
        scores = self.__sentiment_analyzer.get_score(text)
        writer.add_document(id=comment['id'],
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
        for comment in video['comments']:
            scores = self.add_comment(writer, comment['topLevelComment'])
            weight = comment['topLevelComment']['likes'] + 1
            video_scores += numpy.array(scores) * weight
            L += weight
            if replies := comment.get('replies'):
                for reply in replies:
                    self.add_comment(writer, reply)
        video_scores /= L
        writer.add_document(kind='video',
                        id=video['video']['id'],
                        publishedAt=dateutil.parser.isoparse(video['video']['publishedAt']),
                        title=video['video']['title'],
                        likes=video['video']['likes'],
                        content=video['video']['description'],
                        negative=video_scores[0],
                        neutral=video_scores[1],
                        positive=video_scores[2]
                        )

    def write(self, data_dir):
        if self.__ix is not None:
            i = 0
            max_files = 21
            with self.__ix.writer() as w:
                for filename in os.listdir(data_dir):
                    i += 1
                    filepath = os.path.join(data_dir, filename)
                    print(f'Indexing file ({i}/{max_files}): {filename} - {os.path.getsize(filepath)} bytes')
                    # For debugging
                    if (i >= max_files):
                        break
                    with w.group():
                        self.index_video(w, filepath)
                print("Writing the index...")