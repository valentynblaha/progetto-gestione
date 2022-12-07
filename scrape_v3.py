from googleapiclient.discovery import build
import scrapetube
import os
import json

api_key = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'
channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"
dir_files = os.path.join(os.getcwd(), "files")
youtube = build('youtube', 'v3', developerKey=api_key)

def start_crawling():
    video_ids = scrapetube.get_channel("UC8butISFwT-Wl7EV0hUK0BQ")
    ids = []
    for id in video_ids:
        ids.append(str(id['videoId']))
    #create_ids_file(ids)
    return ids

def get_videos_info():
    file_json = os.path.join(dir_files, "videos_inf.json")
    file = open(file_json, 'w')
    #vid_ids = start_crawling()
    videos = get_videos(['Z1N9JzNax2k', '7f50sQYjNRA'])
    for vid in videos:
        file.write(f"{json.dumps(vid)}\n")
    file.close()

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
        'author': comment_snippet['authorDisplayName'],
        'text': comment_snippet['textDisplay'],
        'likes': comment_snippet['likeCount']
    }


def get_comments(videoID):
    comments = []

    def get_request(page_token):
        return youtube.commentThreads().list(
            part='snippet,replies',
            videoId=videoID,
            order='time',  # Time retrieves data faster compared to relevance (default)
            maxResults=100,
            pageToken=page_token,
            textFormat='plainText'
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


# TODO: testing of the following function
def get_videos(videoIDs: list[str]):
    request = youtube.videos().list(
        id=','.join(videoIDs),
        part='id,snippet,contentDetails,statistics',
        maxResults=50
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        videos.append({
            'id': item['id'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'duration': item['contentDetails']['duration'],
            'likes': item['statistics']['likeCount'],
            'views': item['statistics']['viewCount']
        })
    return videos


# WARNING: executing this will reduce the available points for further uses of the API




id = '7f50sQYjNRA'
comments = get_comments(id)
videos1 = get_videos(['tujhGdn1EMI','7f50sQYjNRA'])
print(len(comments))
print(comments)
#for video in videos1:
 #   print(video)
get_videos_info()
#start_crawling()


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