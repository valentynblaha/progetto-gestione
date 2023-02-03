import os
import json
import sentiment_analysis
import numpy

video_id = 'wTuymXD0mNE'

YELLOW='\033[1;33m'
NC='\033[0m' # No Color

with open(os.path.join(os.getcwd(), f'data/{video_id}.json'), 'r') as f:
    json_data = json.loads(f.read())

comments = [comment['topLevelComment'] for comment in json_data['comments']]
i = 0
L = 0
video_scores = numpy.zeros(3)
for comment in comments:
    i += 1
    text = comment['text']
    scores = numpy.array(sentiment_analysis.score_text(text))
    weight = int(comment['likes']) + 1
    video_scores += scores * weight
    L += weight
    print(YELLOW, f'{comment["author"]}', NC)
    print(text)
    print('Scores: ', scores)
video_scores /= L
print('Video score: ', video_scores)