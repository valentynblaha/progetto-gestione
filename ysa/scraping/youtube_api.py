"""
Module containing the YouTube API
"""
from googleapiclient.discovery import build


API_KEY = 'AIzaSyD-u-cmOMhu0jxnOme5mizTWGQHzoM0X8c'
youtube = build('youtube', 'v3', developerKey=API_KEY)
