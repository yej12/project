"""Phase 3 검증: 유튜브 수집기 테스트"""
import sys
from dotenv import load_dotenv
from collectors.youtube_collector import collect_youtube_references

load_dotenv()


def test_youtube_collector(keyword: str = "브랜드 스토리텔링"):
    print(f"=== 유튜브 레퍼런스 수집: '{keyword}' ===\n")
    try:
        results = collect_youtube_references(keyword, max_results=5)
    except ValueError as e:
        print(f"  오류: {e}")
        print("  .env 파일에 YOUTUBE_API_KEY를 설정하세요.")
        return

    if not results:
        print("  결과 없음.")
        return

    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    채널  : {r['channel']}")
        print(f"    설명  : {r['description'][:80]}...")
        print(f"    URL   : {r['url']}")
        print()

    print(f"총 {len(results)}개 수집 완료.")


if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "브랜드 스토리텔링"
    test_youtube_collector(keyword)
