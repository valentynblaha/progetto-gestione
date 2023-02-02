from . import youtube_api
from pathlib import Path
import os, json

api_key = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'

#TODO: make private to package (if possible)
def comment_to_dict(comment_snippet):
    return {
        #TODO: add id as well and consider datetimes
        'author':   comment_snippet['authorDisplayName'],
        'text':     comment_snippet['textDisplay'],
        'likes':    comment_snippet['likeCount']
    }


def scrape_comments(video_id: str):
    """Scrape all the comments of the YouTube video with the given id

    Arguments:
        video_id -- id of the video
    Returns:
        A list of comments with each comment having its replies
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


def scrape_videos_comments(videos_json: str, target_dir: str):
    """Scrape all the comments for each video in the video_json file.
    Each video gets its own file named video_id.json (Replace video_id with video's id),
    and put in target_dir.

    Arguments:
        videos_json -- JSON file with videos
        target_dir -- Directory that will contain the comments
    """
    Path(target_dir).mkdir(parents=True, exist_ok=True)
        
    current_files = {f[:-5] for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))}

    with open(videos_json) as f:
        videos = json.loads(f.read())
        for video in videos:
            id = video['id']
            if id not in current_files:
                record = {'video': video}
                record['comments'] = scrape_comments(video['id'])
                with open(os.path.join(os.getcwd(), f'{target_dir}/{id}.json'), 'w') as video_file:
                    video_file.write(json.dumps(record))
                    print(f'{id}.json written')