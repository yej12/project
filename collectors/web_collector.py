import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


QUERY_TEMPLATES = [
    "{keyword} 브랜드 사례 성공 전략",
    "{keyword} 성공 사례 2024 2025",
    "{keyword} 캠페인 사례 글로벌 브랜드",
    "best {keyword} brand campaign case study",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MarketingBot/1.0)"}


def _fetch_page_content(url: str, max_chars: int = 1500) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ").split())
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

                    content = _fetch_page_content(url)
                    results.append({
                        "title": r.get("title", ""),
                        "url": url,
                        "summary": content if content else r.get("body", ""),
                        "query": query,
                    })
            except Exception as e:
                print(f"  [웹 검색 오류] {query}: {e}")

    return results
