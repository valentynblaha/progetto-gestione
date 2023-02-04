from . import youtube_api
from pathlib import Path
import os, json


def __comment_to_dict(comment):
    comment_snippet = comment['snippet']
    return {
        'id':           comment['id'],
        'publishedAt':  comment_snippet['publishedAt'],
        'author':       comment_snippet['authorDisplayName'],
        'text':         comment_snippet['textDisplay'],
        'likes':        comment_snippet['likeCount']
    }


def scrape_comments(video_id: str) -> list:
    """Scrape all the comments of the YouTube video with the given id

    Args:
        video_id (str): id of the video
    Returns:
        list: Comments with each comment having its replies
    """
    comments = []

    def get_request(page_token: str):
        return youtube_api.youtube.commentThreads().list(
            part        = 'snippet,replies',
            videoId     = video_id,
            order       = 'time', # Time retrieves data faster compared to relevance (default)
            maxResults  = 100,
            pageToken   = page_token,
            textFormat  = 'plainText'
        )

    def append_from_response(response):
        for item in response['items']:
            comment = {}
            comment['topLevelComment'] = __comment_to_dict(item['snippet']['topLevelComment'])
            # Add replies to that comment as well
            if item.get('replies'):
                comment['replies'] = []
                for reply in item['replies']['comments']:
                    comment['replies'].append(__comment_to_dict(reply))
            comments.append(comment)

    request = get_request(None)
    response = request.execute()
    append_from_response(response)
    while response.get('nextPageToken'):
        request = get_request(response['nextPageToken'])
        response = request.execute()
        append_from_response(response)

    return comments


def scrape_videos_comments(videos_json: str, target_dir: str):
    """Scrape all the comments for each video in the video_json file.
    Each video gets its own file named video_id.json (Replace video_id with video's id),
    and put in target_dir.

    Args:
        videos_json (str): JSON file with videos
        target_dir (str): Directory that will contain the comments
    """
    Path(target_dir).mkdir(parents=True, exist_ok=True)
        
    current_files = {f[:-5] for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))}

    with open(videos_json) as f:
        videos = json.loads(f.read())
        i = 0
        for video in videos:
            i += 1
            id = video['id']
            if id not in current_files:
                record = {'video': video}
                record['comments'] = scrape_comments(video['id'])
                with open(os.path.join(os.getcwd(), f'{target_dir}/{id}.json'), 'w') as video_file:
                    video_file.write(json.dumps(record))
                    print(f'({i}/{len(videos)}) {id}.json written')