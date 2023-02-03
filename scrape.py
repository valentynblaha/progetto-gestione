from scraping import videos, comments

channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"
videos_cache_file = 'videos.json'
#videos.create_ids_file(videos.start_crawling(channel_id))

#Videos scraping
videos.cache_videos('links.txt', videos_cache_file)

#Comments scraping
comments.scrape_videos_comments(videos_cache_file, 'data_new')