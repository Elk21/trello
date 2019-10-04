import requests
from config import YOUTUBE_TOKEN


def get_trailer(text):
    '''
        Search YouTube for < film name > trailer and return top 2 results
        Returns array of dicts with title, link and thumbnails image
    '''

    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=2&q={text} trailer&key={YOUTUBE_TOKEN}'

    vids = requests.get(url).json()
    videos = []
    for video in vids['items']:
        result = {}
        result['title'] = video['snippet']['title']
        result['link'] = 'https://www.youtube.com/watch?v=' + \
            video['id']['videoId']
        result['img'] = video['snippet']['thumbnails']['high']['url']
        videos.append(result)

    return videos
