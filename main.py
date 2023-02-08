from scraping import video_scrape, comments_scrape

channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"
videos_cache_file = 'videos.json'
videos_scrape = video_scrape.VideosScraper(channel_id)
videos_scrape.start_crawling()
#Videos scraping
videos_scrape.cache_videos(videos_cache_file)

#Comments scraping
comments = comments_scrape.CommentsScraper('data_new',videos_cache_file)
comments.scrape_videos_comments()