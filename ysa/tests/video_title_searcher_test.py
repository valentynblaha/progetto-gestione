import json
query = 'java'
with open('cache/videos.json', 'r') as f:
    videos = json.loads(f.read())
    i = 0
    for video in videos:
        title = video['title']
        if query in title.lower():
            print(title)
            i += 1
    print('Found', i, 'videos')