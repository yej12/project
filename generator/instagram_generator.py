import os
from groq import Groq


SYSTEM_PROMPT = """You are an Instagram content strategist specializing in marketing and branding.
Generate Instagram content ideas in Korean based on the provided references.

STRICT RULES:
- Write everything in Korean only
- Never use abstract descriptions like "마케팅의 특징을 소개합니다"
- Always cite real brand examples (Apple, Nike, Patagonia, Coca-Cola, etc.) with specific campaigns
- Include concrete numbers, stories, or facts
- Focus on 2024-2025 marketing trends
- Topic must be about marketing/branding only

Output EXACTLY 10 ideas using this format (no deviation):

1. 콘텐츠 유형: 카드뉴스
후킹 문구: (specific hook with brand name or number)
본문 방향: (2-3 lines with concrete examples)
참고 브랜드: (Brand — Campaign name)
해시태그: #tag1 #tag2 #tag3 #tag4 #tag5

2. 콘텐츠 유형: 릴스
..."""


def generate_instagram_content(keyword: str, references: list[dict]) -> list[dict]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY 환경변수가 설정되지 않았습니다.")

    client = Groq(api_key=api_key)
    ref_text = _format_references(references)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=4096,
        temperature=0.7,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"{ref_text}\n\n키워드: '{keyword}'\n위 레퍼런스를 바탕으로 인스타그램 콘텐츠 아이디어 10개를 정해진 형식으로 작성하세요.",
            },
        ],
    )

    raw = response.choices[0].message.content
    return _parse_ideas(raw)


def _format_references(references: list[dict]) -> str:
    lines = ["## 마케팅 레퍼런스\n"]
    for i, r in enumerate(references, 1):
        lines.append(f"[{i}] {r.get('title', '')}")
        body = r.get("summary") or r.get("description", "")
        if body:
            lines.append(f"    {body[:500]}")
        lines.append("")
    return "\n".join(lines)


def _parse_ideas(raw: str) -> list[dict]:
    ideas = []
    current = {}

    for line in raw.splitlines():
        line = line.strip().lstrip("*").rstrip("*").strip()
        if not line:
            continue

        # 번호로 시작하는 새 아이디어
        if line and line[0].isdigit() and ("." in line[:3] or "." in line[:4]):
            if current.get("hook") or current.get("type"):
                ideas.append(current)
            current = {}
            continue

        # 필드 파싱 (볼드 마크다운 제거 후 매칭)
        clean = line.replace("**", "")
        if clean.startswith("콘텐츠 유형:"):
            current["type"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("후킹 문구:"):
            current["hook"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("본문 방향:"):
            current["body"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("참고 브랜드:"):
            current["brand"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("해시태그:"):
            current["hashtags"] = clean.split(":", 1)[1].strip()
        elif current.get("body") and not any(clean.startswith(k) for k in ["콘텐츠", "후킹", "본문", "참고", "해시"]):
            # 본문 방향이 여러 줄일 경우 이어붙임
            current["body"] += " " + clean

    if current.get("hook") or current.get("type"):
        ideas.append(current)

    return ideas
