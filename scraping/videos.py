import scrapetube
import os
import json
from . import youtube_api


def start_crawling(channel_id: str): #TODO: docs
    
    videos = scrapetube.get_channel(channel_id)
    ids = []
    print('')
    for video in videos:
        id = str(video['videoId'])
        ids.append(id)
        print(f'\033[AScraping video: {id}\033[K')
    return ids


def create_ids_file(ids: list[str]): # TODO: docs
    file_txt = os.path.join(os.getcwd(), "links.txt")
    with open(file_txt, 'w') as f:
        f.write('\n'.join(ids))


def scrape_videos(video_ids: list[str]):
    """Scrapes all the videos in videos_ids and returns them in a list.

    Arguments:
        video_ids -- A list of videos to scrape

    Returns:
        A list of scraped videos. Each video is a dictionary. Refer to README file for more info
    """
    request = youtube_api.youtube.videos().list(
        id          = ','.join(video_ids),
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


def cache_videos(ids_filename: str, videos_filename: str):
    """Given a file containing a list of YouTube video's ids (one on each row), 
    scrapes all the videos in that list and writes them to a file named videos_filename.

    Arguments:
        ids_filename -- Name of the file containing the ids
        videos_filename -- Name of the the file that will contain the scraped videos
    """
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