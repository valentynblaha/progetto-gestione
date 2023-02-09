__all__ = ['VideosScraper', 'CommentsScraper', 'youtube_api']

from pathlib import Path
from . import youtube_api

import scrapetube
import os
import json


class VideosScraper:
    
    def __init__(self, id ):
        self.__channel_id = id
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
            id = str(video['videoId'])
            self.__video_ids.append(id)
            print(f'\033[Acrawling video: {id}\033[K')
        self.__create_ids_file()



    def __create_ids_file(self): 
        """
        transfer list of video ids on file 

        Args:
            ids (list[str]): video ids 
        """
        file_txt = os.path.join(os.getcwd(), self.__links_file)
        with open(file_txt, 'w') as f:
            f.write('\n'.join(self.__video_ids))


    def scrape_videos(self,video_ids: list[str]):
        """Scrapes all the videos in videos_ids.

        Args:
            video_ids (list[str]): A list of videos ids to scrape

        Returns:
            list : scraped contents of videos of ids passed  
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
        with open(self.__links_file, 'r') as f:
            video_ids = [line.strip() for line in f]
            n = 0
            while ids := video_ids[n:n + chunk_size]:
                videos += self.scrape_videos(ids)
                n += chunk_size
        print(len(videos)) # For debugging
        with open(videos_filename, 'w') as f:
            f.write(json.dumps(videos))


class CommentsScraper:
     
    def __init__(self, tar , file):
        self.__target_dir = tar
        self.__videos_file = file


    def __comment_to_dict(self,comment):
        comment_snippet = comment['snippet']
        return {
            'id':           comment['id'],
            'publishedAt':  comment_snippet['publishedAt'],
            'author':       comment_snippet['authorDisplayName'],
            'text':         comment_snippet['textDisplay'],
            'likes':        comment_snippet['likeCount']
        }
    
    def __get_request(self,page_token: str , video_id: str):
            return youtube_api.youtube.commentThreads().list(
                part        = 'snippet,replies',
                videoId     = video_id,
                order       = 'time', # Time retrieves data faster compared to relevance (default)
                maxResults  = 100,
                pageToken   = page_token,
                textFormat  = 'plainText'
            )


    def __scrape_comments(self,video_id: str) -> list:
        """Scrape all the comments of the YouTube video with the given id

        Args:
            video_id (str): id of the video
        Returns:
            list: Comments with each comment having its replies
        """
        comments = []
        """

        def get_request(page_token: str):
            return youtube_api.youtube.commentThreads().list(
                part        = 'snippet,replies',
                videoId     = video_id,
                order       = 'time', # Time retrieves data faster compared to relevance (default)
                maxResults  = 100,
                pageToken   = page_token,
                textFormat  = 'plainText'
            )
        """
        def append_from_response(response):
            for item in response['items']:
                comment = {}
                comment['topLevelComment'] = self.__comment_to_dict(item['snippet']['topLevelComment'])
                # Add replies to that comment as well
                if item.get('replies'):
                    comment['replies'] = []
                    for reply in item['replies']['comments']:
                        comment['replies'].append(self.__comment_to_dict(reply))
                comments.append(comment)

        request = self.__get_request(None,video_id)
        response = request.execute()
        append_from_response(response)
        while response.get('nextPageToken'):
            request = self.__get_request(response['nextPageToken'],video_id)
            response = request.execute()
            append_from_response(response)

        return comments


    def scrape_videos_comments(self):
        """Scrape all the comments for each video in the video_json file.
        Each video gets its own file named video_id.json (Replace video_id with video's id),
        and put in target_dir.

        Args:
            videos_json (str): JSON file with videos
            target_dir (str): Directory that will contain the comments
        """
        Path(self.__target_dir).mkdir(parents=True, exist_ok=True)
            
        current_files = {f[:-5] for f in os.listdir(self.__target_dir) if os.path.isfile(os.path.join(self.__target_dir, f))}

        with open(self.__videos_file) as f:
            videos = json.loads(f.read())
            i = 0
            for video in videos:
                i += 1
                id = video['id']
                if id not in current_files:
                    record = {'video': video}
                    record['comments'] = self.__scrape_comments(video['id'])
                    with open(os.path.join(os.getcwd(), f'{self.__target_dir}/{id}.json'), 'w') as video_file:
                        video_file.write(json.dumps(record))
                        print(f'({i}/{len(videos)}) {id}.json written')
    