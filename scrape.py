from googleapiclient.discovery import build
import json

api_key = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'

youtube = build('youtube', 'v3', developerKey = api_key)

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
            comments.append(comment_to_dict(item['snippet']['topLevelComment']['snippet']))
            # Add replies to that comment as well
            if item.get('replies'):
                for reply in item['replies']['comments']:
                    comments.append(comment_to_dict(reply['snippet']))

    request = get_request(None)
    response = request.execute()
    append_from_response(response)
    while response.get('nextPageToken'):
        request = get_request(response['nextPageToken'])
        response = request.execute()
        append_from_response(response)
    
    return comments

# WARNING: executing this will reduce the available points for further uses of the API
comments = get_comments('Yxg96Re2X7k')
f = open('Yxg96Re2X7k.json', 'w')
f.write(json.dumps(comments))
f.close()
print(len(comments))