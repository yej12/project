import os
from groq import Groq


SYSTEM_PROMPT = """당신은 인스타그램 콘텐츠 전략 전문가입니다.
마케팅/브랜딩 레퍼런스를 분석하여 인스타그램 콘텐츠 아이디어를 제안합니다.

각 아이디어는 반드시 아래 형식으로 작성하세요:

[번호]. 콘텐츠 유형: 카드뉴스 / 릴스 / 사진 중 하나
후킹 문구: 첫 줄에 시선을 끄는 문장
본문 방향: 콘텐츠에서 다룰 핵심 내용 2~3줄
해시태그: #태그1 #태그2 #태그3 (5개 이상)"""


def generate_instagram_content(keyword: str, references: list[dict]) -> list[dict]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY 환경변수가 설정되지 않았습니다.")

    client = Groq(api_key=api_key)
    ref_text = _format_references(references)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=4096,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"{ref_text}\n\n위 레퍼런스를 바탕으로 '{keyword}' 주제의 인스타그램 콘텐츠 아이디어 10개를 제안해주세요.",
            },
        ],
    )

    raw = response.choices[0].message.content
    return _parse_ideas(raw)


def _format_references(references: list[dict]) -> str:
    lines = ["## 수집된 마케팅 레퍼런스\n"]
    for i, r in enumerate(references, 1):
        lines.append(f"[{i}] {r.get('title', '')}")
        if r.get("summary") or r.get("description"):
            lines.append(f"    {r.get('summary') or r.get('description', '')[:200]}")
        if r.get("url"):
            lines.append(f"    {r['url']}")
        lines.append("")
    return "\n".join(lines)


def _parse_ideas(raw: str) -> list[dict]:
    ideas = []
    current = {}

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        if line and line[0].isdigit() and "." in line[:3]:
            if current:
                ideas.append(current)
            current = {"raw": line}
        elif line.startswith("콘텐츠 유형:"):
            current["type"] = line.replace("콘텐츠 유형:", "").strip()
        elif line.startswith("후킹 문구:"):
            current["hook"] = line.replace("후킹 문구:", "").strip()
        elif line.startswith("본문 방향:"):
            current["body"] = line.replace("본문 방향:", "").strip()
        elif line.startswith("해시태그:"):
            current["hashtags"] = line.replace("해시태그:", "").strip()

    if current:
        ideas.append(current)

    return ideas
