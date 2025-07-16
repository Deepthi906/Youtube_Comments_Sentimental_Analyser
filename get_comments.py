# get_comments.py
from googleapiclient.discovery import build

from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path[1:]
    return None


def get_comments(video_url, api_key):
    video_id = extract_video_id(video_url)
    youtube = build('youtube', 'v3', developerKey=api_key)
    # Initialize YouTube API client
    service = build('youtube', 'v3', developerKey=api_key)
    comments = []
    request = service.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request:
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        request = service.commentThreads().list_next(request, response)

    return comments

