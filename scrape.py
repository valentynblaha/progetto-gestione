from googleapiclient.discovery import build
import scrapetube
import os
import json

api_key = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'
channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"
dirname = os.path.dirname(__file__)
dir_files = os.path.join(os.getcwd(), "files")
youtube = build('youtube', 'v3', developerKey=api_key)

def start_crawling():
    video_ids = scrapetube.get_channel("UC8butISFwT-Wl7EV0hUK0BQ")
    ids = []
    for id in video_ids:
        ids.append(str(id['videoId']))
    #create_ids_file(ids)
    return ids

def create_ids_file(ids):
    if not os.path.exists(dir_files):
        os.mkdir(dir_files)
        print(dir_files)
    file_txt = os.path.join(dir_files, "links.txt")
    print(file_txt)
    file = open(file_txt, 'w')
    for id in ids:
        file.write(f"{id}\n")


def comment_to_dict(comment_snippet):
    return {
        'author':   comment_snippet['authorDisplayName'],
        'text':     comment_snippet['textDisplay'],
        'likes':    comment_snippet['likeCount']
    }


def get_comments(videoID):
    comments = []

    def get_request(page_token):
        return youtube.commentThreads().list(
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


def get_videos(videoIDs: list[str]):
    request = youtube.videos().list(
        id          = ','.join(videoIDs),
        part        = 'id,snippet,contentDetails,statistics',
        maxResults  = 50
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        videos.append({
            'id':           item['id'],
            'title':        item['snippet']['title'],
            'description':  item['snippet']['description'],
            'duration':     item['contentDetails']['duration'],
            'likes':        item['statistics'].get('likeCount') or 0,
            'views':        item['statistics']['viewCount']
        })
    return videos


# WARNING: executing this will reduce the available points for further uses of the API
"""
id = 'PsNr8CFtMkQ'
comments = get_comments(id)
f = open(f'{id}.json', 'w')
f.write(json.dumps(comments))
f.close()
print(len(comments))
"""

"""
with open('someids.txt', 'r') as f:
    ids = [line.strip() for line in f]
    videos = get_videos(ids)
    print(len(videos))
"""

def cache_videos(ids_file):
    chunk_size = 50
    videos = []
    with open(ids_file, 'r') as f:
        video_ids = [line.strip() for line in f]
        n = 0
        while ids := video_ids[n:n + chunk_size]:
            videos += get_videos(ids)
            n += chunk_size
    print(len(videos)) # For debugging
    with open('videos.json', 'w') as f:
        f.write(json.dumps(videos))
#cache_videos('links.txt')

def get_videos_comments():
    path = os.path.join(dirname, 'data')
    current_files = {f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))}

    with open('videos.json') as f:
        videos = json.loads(f.read())
        for video in videos:
            id = video['id']
            if id not in current_files:
                record = {'video': video}
                record['comments'] = get_comments(video['id'])
                with open(os.path.join(dirname, f'data/{id}.json'), 'w') as video_file:
                    video_file.write(json.dumps(record))
                    print(f'{id}.json written')
get_videos_comments()