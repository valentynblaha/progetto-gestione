from ysa.scraping.youtube_api import youtube

request = youtube.search().list(
    part = 'snippet',
    channelId = 'UC8butISFwT-Wl7EV0hUK0BQ',
    maxResults = 10,
    q = 'html',
    #publishedAfter = '2022-02-07T00:00:00Z',
    type = 'video'
)
response = request.execute()

qn = 8
with open(f'benchmarking/queries_dcg/{qn}.txt', 'a') as f:
    for item in response['items']:
        id = item['id']['videoId']
        f.write(f'{id}\n')
        print(id)