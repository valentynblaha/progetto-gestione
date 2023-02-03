# Progetto gestione dell'informazione

## How to scrape all the comments for a video?

Use the **scrape_comments(video_id)** function from the **scraping.comments** module. It returns a list of comments (which are dictionaries with author, text and likes keys). Be aware that it makes multiple calls to the API in order to retrieve all the pages of comments, therefore it has a quota cost depending on how many pages a video has (100 comments per page). See this link for explanation: https://developers.google.com/youtube/v3/getting-started#quota

## Code documentation
All the Python files are documented using Google Docstrings. For more information on that refer to this link: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings

## Schema of a document
Documents in the **data** directory are in the JSON format. This is their schema:
> **_NOTE_**: The documents are encoded using UTF-8, however the actual characters in strings are backslash escaped (i.e. you won't be able to see emojis in the JSON files themselves). This does not affect the parsing of a document in Python
```json
{
    "video": {
        "id": "string",
        "publishedAt": "string (ISO 8601 format)",
        "title": "string",
        "description": "string",
        "duration": "string (ISO 8601 format)",
        "likes": "number",
        "views": "number"
    },
    "comments": [
        {
            "topLevelComment": "Comment",
            "replies": [
                "Comment"
            ]
        }
    ]
}
```
Here is the schema for a **Comment** element:
```json
{
    "id": "string",
    "publishedAt": "string (ISO 8601 format)",
    "author": "string",
    "text": "string",
    "likes": "number"
}
```
