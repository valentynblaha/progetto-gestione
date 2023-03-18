"""
Module containing the YouTube API
"""
from googleapiclient.discovery import build

raise Exception("Valid API Key needed")
# replace the empty string in the following line with a valid YouTube Data API Key
API_KEY = ''
youtube = build('youtube', 'v3', developerKey=API_KEY)
