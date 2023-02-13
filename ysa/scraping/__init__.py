"""
Package for scraping information from videos (i.e. title, description, publication date etc...)
and their comments on YouTube
"""
__all__ = ['VideosScraper', 'CommentsScraper', 'youtube_api']

from pathlib import Path

import os
import json
import scrapetube

from . import youtube_api


class VideosScraper:
    """Class containing methods for scraping all the videos from a YouTube channel
    """

    def __init__(self, channel_id):
        self.__channel_id = channel_id
        self.__video_ids = []
        self.__links_file = "links.txt"

    def start_crawling(self):
        """
        when passed channel id of a youtube channel this funtion performs crawling to
        extract all the ids of videos uploaded on the channel from their respected 
        urls to perform crawling later

        Args:
            channel_id (str): string of channel id

        Returns:
            list : video ids
        """

        videos = scrapetube.get_channel(self.__channel_id)

        print('')
        for video in videos:
            video_id = str(video['videoId'])
            self.__video_ids.append(video_id)
            print(f'\033[Acrawling video: {video_id}\033[K')
        self.__create_ids_file()

    def __create_ids_file(self):
        """
        transfer list of video ids on file 

        Args:
            ids (list[str]): video ids 
        """
        file_txt = os.path.join(os.getcwd(), self.__links_file)
        with open(file_txt, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.__video_ids))

    def scrape_videos(self, video_ids: list[str]):
        """Scrapes all the videos in videos_ids.

        Args:
            video_ids (list[str]): A list of videos ids to scrape

        Returns:
            list : scraped contents of videos of ids passed  
        """
        request = youtube_api.youtube.videos().list(
            id=','.join(video_ids),
            part='id,snippet,contentDetails,statistics',
            maxResults=50
        )
        response = request.execute()
        videos = []
        for item in response['items']:
            videos.append({
                'id':           item['id'],
                'publishedAt':  item['snippet']['publishedAt'],
                'title':        item['snippet']['title'],
                'description':  item['snippet']['description'],
                'duration':     item['contentDetails']['duration'],
                'likes':        item['statistics'].get('likeCount') or 0,
                'views':        item['statistics']['viewCount']
            })
        return videos

    def cache_videos(self, videos_filename: str):
        """Given a file containing a list of YouTube video's ids (one on each row), 
        scrapes all the videos in that list and writes them to a file named videos_filename.

        Args:
            ids_filename (str): Name of the file containing the ids
            videos_filename (str): Name of the the file that will contain the scraped videos
        """
        chunk_size = 50
        videos = []
        with open(self.__links_file, 'r', encoding='utf-8') as f:
            video_ids = f.read().splitlines()
        n = 0
        while ids := video_ids[n:n + chunk_size]:
            videos += self.scrape_videos(ids)
            n += chunk_size
        print(len(videos))  # For debugging
        with open(videos_filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(videos))


class CommentsScraper:
    """Class containing methods for scraping all the commments from a list
    of videos given by a previously cached file using the VideoScraper
    """

    def __init__(self, target_dir, videos_cache_file):
        self.__target_dir = target_dir
        self.__videos_file = videos_cache_file

    def __comment_to_dict(self, comment):
        comment_snippet = comment['snippet']
        return {
            'id':           comment['id'],
            'publishedAt':  comment_snippet['publishedAt'],
            'author':       comment_snippet['authorDisplayName'],
            'text':         comment_snippet['textDisplay'],
            'likes':        comment_snippet['likeCount']
        }

    def __get_request(self, page_token: str, video_id: str):
        return youtube_api.youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            # Time retrieves data faster compared to relevance (default)
            order='time',
            maxResults=100,
            pageToken=page_token,
            textFormat='plainText'
        )

    def __scrape_comments(self, video_id: str) -> list:
        """Scrape all the comments of the YouTube video with the given id

        Args:
            video_id (str): id of the video
        Returns:
            list: Comments with each comment having its replies
        """
        comments = []

        def append_from_response(response):
            for item in response['items']:
                comment = {}
                comment['topLevelComment'] = self.__comment_to_dict(
                    item['snippet']['topLevelComment'])
                # Add replies to that comment as well
                if item.get('replies'):
                    comment['replies'] = []
                    for reply in item['replies']['comments']:
                        comment['replies'].append(
                            self.__comment_to_dict(reply))
                comments.append(comment)

        request = self.__get_request(None, video_id)
        response = request.execute()
        append_from_response(response)
        while response.get('nextPageToken'):
            request = self.__get_request(response['nextPageToken'], video_id)
            response = request.execute()
            append_from_response(response)

        return comments

    def scrape_videos_comments(self):
        """Scrape all the comments for each video in the video_json file.
        Each video gets its own file named video_id.json (Replace video_id with video's id),
        and put in target_dir.
        """
        Path(self.__target_dir).mkdir(parents=True, exist_ok=True)

        current_files = {f[:-5] for f in os.listdir(
            self.__target_dir) if os.path.isfile(os.path.join(self.__target_dir, f))}

        with open(self.__videos_file, 'r', encoding='utf-8') as f:
            videos = json.loads(f.read())
            i = 0
            for video in videos:
                i += 1
                video_id = video['id']
                if video_id not in current_files:
                    record = {'video': video}
                    record['comments'] = self.__scrape_comments(video['id'])
                    with open(f'{self.__target_dir}/{video_id}.json', 'w', encoding='utf-8') as video_file:
                        video_file.write(json.dumps(record))
                        print(f'({i}/{len(videos)}) {video_id}.json written')
