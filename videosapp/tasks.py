import json
from videosapp.models import YVideoData
from django.utils import dateparse
from yapis.settings import YOUTUBE_API_KEYS,YOUTUBE_API_URL

from celery import shared_task
from celery.utils.log import get_task_logger
import requests


logger = get_task_logger(__name__)

@shared_task
def youtube_task():
    print("Youtube data is being fetched")
    page_token = ""
    while True:
        params = {
            "part":"snippet",
            "maxResults":50,
            "type":"video",
            "key":"AIzaSyBE8MByQDhGWk_3lSFQszTUxalkgs-z-6Y",
            "pageToken":page_token,
            "publishedAfter":"2015-01-01T00:00:00Z",
            "order":"date",
            "q":"live",
        }
        print("Accessing Youtube Data with API_KEY: ", YOUTUBE_API_KEYS)
        print(YOUTUBE_API_URL)
        response = requests.get(YOUTUBE_API_URL, params=params)
        print(response)
        if response.status_code == 200:
            json_response = response.json()
            
            for i in json_response.get("items", []):
                video_id = i.get("id", {}).get("videoId")
                snippet_data = i.get("snippet", {})
                if snippet_data:
                    print(i)
                    try:
                        p = YVideoData()
                        p.id = video_id
                        if type(i['snippet']['title'])=='str':
                            p.title = str(i['snippet']['title'])
                        else:
                            p.title = 'title not as string'
                        p.description = i['snippet']['description']
                        p.publishing_datetime = dateparse.parse_datetime(i['snippet']['publishedAt'])
                        p.thumbnails_urls = i['snippet']['thumbnails']['default']['url']
                        p.save()
                    except Exception as exc:
                        print("Exception in saving data to db")
                        print("Exception: " + str(exc))
                        return
            print("Youtube data saved to database")