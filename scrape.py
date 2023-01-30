from scraping import videos

# TODO: write all the scraping code

#Video scraping
channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"

videos.create_ids_file(videos.start_crawling(channel_id))
videos.cache_videos('links.txt')

#Comment scraping
