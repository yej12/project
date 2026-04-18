# 마케팅 레퍼런스 수집 + 인스타 콘텐츠 생성 도구

## 목적
키워드를 입력하면 웹과 유튜브에서 마케팅 관련 정보를 수집하고, Claude API를 통해 인스타그램 콘텐츠 아이디어를 리스트업하는 CLI 도구.

## 기술 스택
- **언어**: Python 3.11+
- **웹 검색**: DuckDuckGo Search (`duckduckgo-search`) — API 키 불필요
- **유튜브 검색**: YouTube Data API v3 (`google-api-python-client`) — API 키 필요
- **콘텐츠 생성**: Claude API (`anthropic`, `claude-sonnet-4-6`) — API 키 필요
- **환경변수**: `python-dotenv`

## 프로젝트 구조

```
project/
├── .env                      # API 키 (gitignore)
├── .env.example              # 키 템플릿
├── .gitignore
├── requirements.txt
├── main.py                   # 진입점 CLI
├── collectors/
│   ├── __init__.py
│   ├── web_collector.py      # DuckDuckGo 웹 검색
│   └── youtube_collector.py  # YouTube 검색
├── generator/
│   ├── __init__.py
│   └── instagram_generator.py  # Claude API 콘텐츠 생성
└── CLAUDE.md
```

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

# 실행
python main.py --keyword "제로웨이스트"
python main.py --keyword "비건" --max-results 5
```

## 환경변수 (.env)

```
ANTHROPIC_API_KEY=...
YOUTUBE_API_KEY=...
```

## 개발 계획

### Phase 1 — 프로젝트 초기화
- [ ] `requirements.txt`, `.env.example`, `.gitignore` 생성
- [ ] 패키지 디렉토리 구조 생성 (`collectors/`, `generator/`)

### Phase 2 — 웹 수집기 (`collectors/web_collector.py`)
- [ ] `duckduckgo-search` 라이브러리로 키워드 검색 구현
- [ ] 쿼리 자동 확장: `"{keyword} 마케팅 전략"`, `"{keyword} 캠페인 사례"` 등
- [ ] 결과 파싱: 제목 + URL + 요약 텍스트 반환

### Phase 3 — 유튜브 수집기 (`collectors/youtube_collector.py`)
- [ ] YouTube Data API `search.list` 연동
- [ ] 키워드 기반 마케팅 영상 검색 (최대 10개)
- [ ] 결과 파싱: 영상 제목 + 채널명 + 설명 + URL 반환

### Phase 4 — 인스타 콘텐츠 생성기 (`generator/instagram_generator.py`)
- [ ] 수집 레퍼런스를 Claude API 프롬프트로 조합
- [ ] 인스타그램 포스트 아이디어 10개 생성 (유형 / 후킹 문구 / 본문 방향 / 해시태그)
- [ ] `claude-sonnet-4-6` 모델 + prompt caching 적용

### Phase 5 — CLI 진입점 (`main.py`)
- [ ] `argparse`로 `--keyword`, `--max-results` 옵션 처리
- [ ] 수집 → 생성 파이프라인 연결 및 결과 출력

### Phase 6 — 검증
- [ ] 키워드 입력 → 웹/유튜브 레퍼런스 수집 확인
- [ ] 인스타 콘텐츠 아이디어 10개 정상 출력 확인

---

## 출력 예시

- 수집된 웹 레퍼런스 목록 (제목 + URL + 요약)
- 수집된 유튜브 영상 목록 (제목 + 채널 + URL)
- 인스타그램 콘텐츠 아이디어 10개
  - 콘텐츠 유형 (카드뉴스 / 릴스 / 사진)
  - 후킹 문구
  - 본문 방향
  - 추천 해시태그
