import scrapetube
import os
import json
from . import youtube_api

channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"


def start_crawling():
    video_ids = scrapetube.get_channel(channel_id)
    ids = []
    for id in video_ids:
        ids.append(str(id['videoId']))
    #create_ids_file(ids)
    return ids


def create_ids_file(ids):
    file_txt = os.path.join(os.getcwd(), "links.txt")
    #print(file_txt)
    with open(file_txt, 'w') as f:
        f.write('\n'.join(ids))


def scrape_videos(videoIDs: list[str]):
    request = youtube_api.youtube.videos().list(
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


def cache_videos(ids_filename):
    chunk_size = 50
    videos = []
    with open(ids_filename, 'r') as f:
        video_ids = [line.strip() for line in f]
        n = 0
        while ids := video_ids[n:n + chunk_size]:
            videos += scrape_videos(ids)
            n += chunk_size
    print(len(videos)) # For debugging
    with open('videos.json', 'w') as f:
        f.write(json.dumps(videos))