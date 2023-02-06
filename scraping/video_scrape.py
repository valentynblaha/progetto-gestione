import scrapetube
import os
import json
from . import youtube_api


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