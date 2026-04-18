import os
from googleapiclient.discovery import build


def collect_youtube_references(keyword: str, max_results: int = 10) -> list[dict]:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY 환경변수가 설정되지 않았습니다.")

    youtube = build("youtube", "v3", developerKey=api_key)

    response = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=max_results,
        relevanceLanguage="ko",
        order="relevance",
    ).execute()

    results = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        video_id = item["id"]["videoId"]
        results.append({
            "title": snippet.get("title", ""),
            "channel": snippet.get("channelTitle", ""),
            "description": snippet.get("description", ""),
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })

    return results
