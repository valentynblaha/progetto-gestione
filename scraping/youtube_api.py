from googleapiclient.discovery import build


api_key = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'
youtube = build('youtube', 'v3', developerKey=api_key)
