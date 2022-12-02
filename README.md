# Progetto gestione dell'informazione

## How to scrape all the comments for a video?

Use the **get_comments(videoID)** function. It returns an list of strings (which are the comments). Be aware that it makes multiple calls to the API in order to retrieve all the pages of comments, therefore it has a quota cost depending on how many pages a video has (100 comments per page). See this link for explanation: https://developers.google.com/youtube/v3/getting-started#quota
