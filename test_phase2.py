"""Phase 2 검증: 웹 수집기 테스트"""
from collectors.web_collector import collect_web_references


def test_web_collector(keyword: str = "브랜드 스토리텔링"):
    print(f"=== 웹 레퍼런스 수집: '{keyword}' ===\n")
    results = collect_web_references(keyword, max_results=3)

    if not results:
        print("  결과 없음. 네트워크 연결을 확인하세요.")
        return

    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    URL    : {r['url']}")
        print(f"    요약   : {r['summary'][:80]}...")
        print(f"    쿼리   : {r['query']}")
        print()

    print(f"총 {len(results)}개 수집 완료.")


if __name__ == "__main__":
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "브랜드 스토리텔링"
    test_web_collector(keyword)
