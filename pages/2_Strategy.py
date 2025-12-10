# pages/2_Strategy.py

import streamlit as st

from services.strategy_loader import load_strategies
from services.practice_log import init_practice_state
from components.layout import render_page_header


def main():
    init_practice_state()
    df = load_strategies()

    render_page_header("대비전략", "자주 쓰이는 답변 구조와 전략을 카드 형태로 정리합니다.")

    if "starred_strategies" not in st.session_state:
        st.session_state.starred_strategies = set()

    with st.sidebar:
        st.subheader("📌 전략 필터")
        categories = ["전체"] + sorted(df["category"].unique())
        cat_sel = st.selectbox("카테고리", categories)

        only_starred = st.checkbox("⭐️ 표시한 전략만 보기", value=False)

    filtered = df
    if cat_sel != "전체":
        filtered = filtered[filtered["category"] == cat_sel]

    if only_starred:
        filtered = filtered[filtered["id"].isin(st.session_state.starred_strategies)]

    if filtered.empty:
        st.warning("조건에 맞는 전략이 없습니다. 필터를 조정해 보세요.")
        return

    for _, row in filtered.iterrows():
        strategy_id = row["id"]
        with st.container():
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown(f"### {row['title']}")
                st.caption(f"카테고리: {row['category']}")
            with cols[1]:
                starred = strategy_id in st.session_state.starred_strategies
                new_starred = st.checkbox(
                    "⭐️", value=starred, key=f"star_{strategy_id}"
                )
                if new_starred:
                    st.session_state.starred_strategies.add(strategy_id)
                else:
                    st.session_state.starred_strategies.discard(strategy_id)

            st.markdown("**요약**")
            st.write(row["summary"])

            st.markdown("**답변 구조(서론–본론–결론 틀)**")
            st.write(row["structure"])

            st.markdown("**TIP**")
            st.info(row["tips"])

            st.markdown("---")

    st.info(
        "📚 전략을 충분히 익힌 후, 상단 메뉴에서 **문제 연습** 페이지로 이동해 "
        "실제 문항에 전략을 적용해 보세요."
    )


if __name__ == "__main__":
    main()
