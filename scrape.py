from googleapiclient.discovery import build

api_key = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'

youtube = build('youtube', 'v3', developerKey = api_key)

def get_comments(videoID):
    
    comments = []

    def append_from_response(response):
        for item in response['items']:
            comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            # Add replies to that comment as well
            if item.get('replies'):
                for reply in item['replies']['comments']:
                    comments.append(reply['snippet']['textDisplay'])

    request = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=videoID,
        order='time',
        maxResults=100
    )
    response = request.execute()
    append_from_response(response)
    while response.get('nextPageToken'):
        request = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=videoID,
            order='time',
            pageToken = response['nextPageToken'],
            maxResults=100
        )
        response = request.execute()
        append_from_response(response)
    
    return comments

# WARNING: executing this will reduce the available points for further uses of the API
comments = get_comments('rfscVS0vtbw')
print(len(get_comments('rfscVS0vtbw')))