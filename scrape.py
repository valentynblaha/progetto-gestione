from scraping import videos, comments

#Video scraping
channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"

#videos.create_ids_file(videos.start_crawling(channel_id))
#videos.cache_videos('links.txt', 'videos.json')

#Comment scraping
comments.scrape_videos_comments('videos.json', 'data_new')