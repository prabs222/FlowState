import requests
from django.conf import settings
from django.shortcuts import render

def search_data(string,counter):
    search_url = 'https://www.googleapis.com/youtube/v3/search'

    search_params = {
        'part' : 'snippet',
        'q' : string,
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : counter,
        'type' : 'video'
    }
    response=requests.get(search_url,params=search_params)
    results=response.json()['items']

    random_videos=[]
    for i in results:
        random_videos.append({'title':i['snippet']['title'],'url':f'https://www.youtube.com/watch?v={ i["id"]["videoId"] }','thumbnail':i['snippet']['thumbnails']['default']['url']})

    return random_videos


