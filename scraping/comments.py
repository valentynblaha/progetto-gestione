from . import youtube_api
import os, json

api_key = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'

dirname = os.path.dirname(__file__)

def comment_to_dict(comment_snippet):
    return {
        'author':   comment_snippet['authorDisplayName'],
        'text':     comment_snippet['textDisplay'],
        'likes':    comment_snippet['likeCount']
    }


def scrape_comments(videoID):
    comments = []

    def get_request(page_token):
        return youtube_api.youtube.commentThreads().list(
            part        = 'snippet,replies',
            videoId     = videoID,
            order       = 'time', # Time retrieves data faster compared to relevance (default)
            maxResults  = 100,
            pageToken   = page_token,
            textFormat  = 'plainText'
        )

    def append_from_response(response):
        for item in response['items']:
            comment = {}
            comment['topLevelComment'] = comment_to_dict(item['snippet']['topLevelComment']['snippet'])
            # Add replies to that comment as well
            if item.get('replies'):
                comment['replies'] = []
                for reply in item['replies']['comments']:
                    comment['replies'].append(comment_to_dict(reply['snippet']))
            comments.append(comment)

    request = get_request(None)
    response = request.execute()
    append_from_response(response)
    while response.get('nextPageToken'):
        request = get_request(response['nextPageToken'])
        response = request.execute()
        append_from_response(response)

    return comments


def scrape_videos_comments(videos_json): # TODO: make target dir argument
    path = os.path.join(dirname, 'data')
    current_files = {f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))}

    with open(videos_json) as f:
        videos = json.loads(f.read())
        for video in videos:
            id = video['id']
            if id not in current_files:
                record = {'video': video}
                record['comments'] = scrape_comments(video['id'])
                with open(os.path.join(dirname, f'data/{id}.json'), 'w') as video_file:
                    video_file.write(json.dumps(record))
                    print(f'{id}.json written')