from duckduckgo_search import DDGS


QUERY_TEMPLATES = [
    "{keyword} 사례",
    "{keyword} 트렌드",
    "{keyword} 성공 사례",
    "{keyword} 인스타그램 콘텐츠",
]


def collect_web_references(keyword: str, max_results: int = 5) -> list[dict]:
    results = []
    seen_urls = set()

    with DDGS() as ddgs:
        for template in QUERY_TEMPLATES:
            query = template.format(keyword=keyword)
            try:
                for r in ddgs.text(query, max_results=max_results):
                    url = r.get("href", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        results.append({
                            "title": r.get("title", ""),
                            "url": url,
                            "summary": r.get("body", ""),
                            "query": query,
                        })
            except Exception as e:
                print(f"  [웹 검색 오류] {query}: {e}")

    return results
