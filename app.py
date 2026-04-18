import streamlit as st
from dotenv import load_dotenv
from collectors.web_collector import collect_web_references
from collectors.youtube_collector import collect_youtube_references
from generator.instagram_generator import generate_instagram_content

load_dotenv()

st.set_page_config(page_title="마케팅 레퍼런스 수집기", page_icon="📱", layout="wide")

st.title("📱 마케팅 레퍼런스 수집 + 인스타 콘텐츠 생성")
st.caption("키워드를 입력하면 웹/유튜브 레퍼런스를 수집하고 인스타그램 콘텐츠 아이디어를 생성합니다.")

keyword = st.text_input("마케팅/브랜딩 키워드 입력", placeholder="예: 바이럴 마케팅, 브랜드 스토리텔링")
col1, col2 = st.columns(2)
max_web = col1.slider("웹 검색 결과 수", 3, 10, 5)
max_yt = col2.slider("유튜브 검색 결과 수", 3, 10, 5)

if st.button("🔍 수집 및 콘텐츠 생성", type="primary", disabled=not keyword):
    references = []

    with st.status("레퍼런스 수집 중...", expanded=True) as status:

        st.write("🌐 웹 검색 중...")
        web_refs = collect_web_references(keyword, max_results=max_web)
        st.write(f"  → {len(web_refs)}개 수집 완료")

        st.write("▶️ 유튜브 검색 중...")
        try:
            yt_refs = collect_youtube_references(keyword, max_results=max_yt)
            st.write(f"  → {len(yt_refs)}개 수집 완료")
        except ValueError as e:
            yt_refs = []
            st.write(f"  → 유튜브 스킵 ({e})")

        references = web_refs + yt_refs

        st.write("✨ 콘텐츠 아이디어 생성 중...")
        ideas = generate_instagram_content(keyword, references)
        st.write(f"  → {len(ideas)}개 생성 완료")

        status.update(label="완료!", state="complete")

    tab1, tab2, tab3 = st.tabs(["📱 콘텐츠 아이디어", "🌐 웹 레퍼런스", "▶️ 유튜브 레퍼런스"])

    with tab1:
        st.subheader(f"'{keyword}' 인스타그램 콘텐츠 아이디어")
        for i, idea in enumerate(ideas, 1):
            with st.expander(f"#{i}  {idea.get('hook', idea.get('raw', ''))}", expanded=i <= 3):
                col_a, col_b = st.columns([1, 2])
                col_a.markdown(f"**유형**")
                col_b.markdown(idea.get("type", "-"))
                col_a.markdown(f"**후킹 문구**")
                col_b.markdown(idea.get("hook", "-"))
                col_a.markdown(f"**본문 방향**")
                col_b.markdown(idea.get("body", "-"))
                col_a.markdown(f"**참고 브랜드**")
                col_b.markdown(idea.get("brand", "-"))
                col_a.markdown(f"**해시태그**")
                col_b.markdown(idea.get("hashtags", "-"))

    with tab2:
        st.subheader("수집된 웹 레퍼런스")
        for r in web_refs:
            st.markdown(f"**[{r['title']}]({r['url']})**")
            st.caption(r.get("summary", "")[:150])
            st.divider()

    with tab3:
        st.subheader("수집된 유튜브 레퍼런스")
        if yt_refs:
            for r in yt_refs:
                st.markdown(f"**[{r['title']}]({r['url']})**")
                st.caption(f"{r['channel']} · {r.get('description', '')[:100]}")
                st.divider()
        else:
            st.info("유튜브 API 키가 없으면 수집되지 않습니다.")
