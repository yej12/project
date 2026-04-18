"""Phase 4 검증: Claude API 인스타 콘텐츠 생성 테스트"""
import sys
from dotenv import load_dotenv
from generator.instagram_generator import generate_instagram_content

load_dotenv()

SAMPLE_REFERENCES = [
    {
        "title": "바이럴 마케팅의 핵심 — 공유되는 콘텐츠의 조건",
        "summary": "감정을 자극하고, 공유할 이유를 주며, 브랜드 메시지를 자연스럽게 녹여야 한다.",
        "url": "https://example.com/viral-marketing",
    },
    {
        "title": "MZ세대가 반응하는 브랜드 스토리텔링 전략",
        "summary": "진정성 있는 스토리, 참여 유도, 짧고 강렬한 메시지가 핵심이다.",
        "url": "https://example.com/mz-brand",
    },
    {
        "title": "인스타그램 릴스로 브랜드 인지도 높인 사례",
        "description": "짧은 영상 포맷으로 제품 사용법과 감성 스토리를 결합한 콘텐츠가 높은 조회수를 기록했다.",
        "url": "https://youtube.com/watch?v=example",
    },
]


def test_generator(keyword: str = "바이럴 마케팅"):
    print(f"=== 인스타 콘텐츠 생성: '{keyword}' ===\n")
    try:
        ideas = generate_instagram_content(keyword, SAMPLE_REFERENCES)
    except ValueError as e:
        print(f"  오류: {e}")
        print("  .env 파일에 ANTHROPIC_API_KEY를 설정하세요.")
        return

    for i, idea in enumerate(ideas, 1):
        print(f"[{i}]")
        print(f"  유형     : {idea.get('type', '-')}")
        print(f"  후킹문구 : {idea.get('hook', '-')}")
        print(f"  본문방향 : {idea.get('body', '-')}")
        print(f"  해시태그 : {idea.get('hashtags', '-')}")
        print()

    print(f"총 {len(ideas)}개 아이디어 생성 완료.")


if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "바이럴 마케팅"
    test_generator(keyword)
