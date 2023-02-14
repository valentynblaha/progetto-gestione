from ysa.scraping.youtube_api import youtube
import json
from ysa.indexing import SentimentAnalyzer

request = youtube.commentThreads().list(
    part='id,replies,snippet',
    allThreadsRelatedToChannelId='UC8butISFwT-Wl7EV0hUK0BQ',
    maxResults=100,
    order='relevance',
    searchTerms='json',
    # publishedAfter = '2022-02-07T00:00:00Z',
    # type = 'video'
)
response = request.execute()
print('Found ', len(response['items']), ' results')

def get_likes(video_id):
    with open(f'data/{video_id}.json', 'r', encoding='utf-8') as f:
        video_json = json.loads(f.read())
        return int(video_json['video']['likes'])


qn = 3
"""
with open(f'benchmarking/queries_dcg/{qn}.txt', 'w') as f:
    l = []
    for item in response['items']:
        id = item['id']['videoId']
        try:
            if (get_likes(id) >= 5000):
                l.append(f'{id}\n')
                print(id)
            else:
                print('Less than 5000 likes: ', id)
        except FileNotFoundError as e:
            print(f'{id} not found')
    f.write('\n'.join(l))
"""

sa = SentimentAnalyzer()


def filter_comments():

    ids = []

    def score_comment(comment):
        score = sa.get_score(comment['snippet']['textDisplay'])
        print(score)
        return score

    def filter_score(score, filter):
        if filter(score):
            if item['snippet']['videoId'] not in ids:
                print(item['snippet']['videoId'])
                ids.append(item['snippet']['videoId'])

    with open(f'benchmarking/queries_dcg/{qn}.txt', 'w') as f:
        items = response['items']
        def filter(s): return s[2] > 0.5
        for item in items:
            filter_score(
                score_comment(item['snippet']['topLevelComment']),
                filter)
            replies = item.get('replies')
            if replies:
                for replie in replies['comments']:
                    filter_score(
                        score_comment(replie), filter
                    )
        f.write('\n'.join(ids))

filter_comments()