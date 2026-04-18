"""Phase 1 검증: 프로젝트 구조 및 의존성 확인"""
import os
import sys


def check_structure():
    required = [
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "collectors/__init__.py",
        "generator/__init__.py",
        "notions/__init__.py",
    ]
    print("=== 디렉토리 구조 확인 ===")
    all_ok = True
    for path in required:
        exists = os.path.exists(path)
        status = "✓" if exists else "✗"
        print(f"  {status} {path}")
        if not exists:
            all_ok = False
    return all_ok


def check_imports():
    print("\n=== 패키지 임포트 확인 ===")
    packages = {
        "anthropic": "anthropic",
        "duckduckgo_search": "duckduckgo-search",
        "googleapiclient": "google-api-python-client",
        "notion_client": "notion-client",
        "dotenv": "python-dotenv",
    }
    all_ok = True
    for module, pkg in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg} — 설치 필요")
            all_ok = False
    return all_ok


def check_env():
    print("\n=== 환경변수 확인 ===")
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()
        print("  ✓ .env 파일 로드됨")
    else:
        print("  ! .env 파일 없음 (.env.example 복사 후 키 입력 필요)")

    keys = ["ANTHROPIC_API_KEY", "YOUTUBE_API_KEY", "NOTION_API_KEY", "NOTION_DATABASE_ID"]
    for key in keys:
        val = os.getenv(key)
        if val and not val.startswith("your_"):
            print(f"  ✓ {key} 설정됨")
        else:
            print(f"  ! {key} 미설정")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ok1 = check_structure()
    ok2 = check_imports()
    check_env()

    print("\n=== 결과 ===")
    if ok1 and ok2:
        print("  Phase 1 완료. Phase 2 진행 가능.")
    else:
        if not ok2:
            print("  pip install -r requirements.txt 를 먼저 실행하세요.")
        sys.exit(1)
