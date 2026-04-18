import re
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


QUERY_TEMPLATES = [
    "{keyword} 브랜드 성공 사례",
    "{keyword} 마케팅 캠페인 사례 2024",
    "best {keyword} brand campaign case study",
    "{keyword} 글로벌 브랜드 전략",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MarketingBot/1.0)"}


def _is_valid_content(text: str) -> bool:
    # 중국어/일본어 비율이 높으면 제외
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3040-\u30ff]', text))
    return cjk / max(len(text), 1) < 0.1


def _fetch_page_content(url: str, max_chars: int = 1500) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ").split())
        if not _is_valid_content(text):
            return ""
        return text[:max_chars]
    except Exception:
        return ""


def collect_web_references(keyword: str, max_results: int = 5) -> list[dict]:
    results = []
    seen_urls = set()

    with DDGS() as ddgs:
        for template in QUERY_TEMPLATES:
            query = template.format(keyword=keyword)
            try:
                for r in ddgs.text(query, max_results=max_results):
                    url = r.get("href", "")
                    if not url or url in seen_urls:
                        continue
                    seen_urls.add(url)

                    snippet = r.get("body", "")
                    if not _is_valid_content(snippet):
                        continue

                    content = _fetch_page_content(url)
                    results.append({
                        "title": r.get("title", ""),
                        "url": url,
                        "summary": content if content else snippet,
                        "query": query,
                    })
            except Exception as e:
                print(f"  [웹 검색 오류] {query}: {e}")

    return results
