from videosapp.models import YVideoData
from django_rq import job

from yapis.settings import (
    YOUTUBE_API_URL,
    YOUTUBE_API_KEYS,
    YOUTUBE_SEARCH_LIST,
)

import requests


@job("default")
def fetch_youtube_data():
    import ipdb;
    ipdb.set_trace()
    # Creating the GET API to query youtube
    print("Task Initiated")
    url = YOUTUBE_API_URL
    api_key_index = 0
    page_token = ""

    # Loop for multiple requests in case of multiple records or api_key exhausted
    while True:
        params = {
            "part": "snippet",
            "maxResults": 50,
            "type": "video",
            "key": YOUTUBE_API_KEYS[api_key_index],
            "pageToken": page_token,
            "publishedAfter": "2018-01-01T00:00:00Z",
            "order": "date",
            "q": "|".join(YOUTUBE_SEARCH_LIST),
        }
        print("Accessing Youtube Data with API_KEY: ", YOUTUBE_API_KEYS[api_key_index])

        try:
            response = requests.get(url, params=params)
        except Exception as exc:
            print("Exception while accessing the search API")
            print("Exception: " + str(exc))
            return

        # If status is 200
        if response.status_code == 200:
            json_response = response.json()

            # Iterating the QuerySet received
            for item in json_response.get("items", []):
                video_id = item.get("id", {}).get("videoId")
                snippet_data = item.get("snippet", {})
                if snippet_data:
                    try:
                        (obj, created) = YVideoData.objects.get_or_create(
                            id=video_id,
                            title=snippet_data.get("title"),
                            description=snippet_data.get("description"),
                            publishing_datetime=snippet_data.get("publishedAt"),
                            defaults={
                                "thumbnails_urls": snippet_data.get("thumbnails", {})
                                .get("default", {})
                                .get("url")
                            },
                        )
                        if created:
                            print("Successfully Created: ", obj.title)
                    except Exception as exc:
                        print("Exception in saving data to db")
                        print("Exception: " + str(exc))
                        return

            # Flag to check if subsequent call is required
            if json_response.get("nextPageToken"):
                page_token = json_response["nextPageToken"]
                continue
            break

        # If status is other than 200
        else:
            print(
                "Issue in Youtube Search Calls, Response: ",
                response.status_code,
                " Params: ",
                params,
            )
            if response.status_code == 403:
                api_key_index += 1
                if api_key_index >= len(YOUTUBE_API_KEYS):
                    print("All API Keys Exhausted")
                    return
                else:
                    continue
            return

    return