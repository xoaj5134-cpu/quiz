# pages/5_Wrong_Note.py

import streamlit as st

from services.practice_log import init_practice_state, get_all_logs, get_wrong_logs
from components.layout import render_page_header


def main():
    init_practice_state()
    all_logs = get_all_logs()
    wrong_logs = get_wrong_logs()

    render_page_header("오답노트 / 연습 기록", "저장한 오답과 전체 연습 기록을 한 곳에서 관리합니다.")

    if not all_logs:
        st.info("아직 저장된 연습 기록이 없습니다. 먼저 문제 연습이나 실전 MMI 모드에서 연습을 진행해 주세요.")
        return

    tab1, tab2 = st.tabs(["📒 오답노트", "📂 전체 기록"])

    with tab1:
        if not wrong_logs:
            st.info("오답노트에 저장된 문항이 없습니다. 연습 시 '오답노트에 저장' 체크를 해보세요.")
        else:
            for i, rec in enumerate(reversed(wrong_logs), start=1):
                with st.expander(
                    f"{i}. [{rec['timestamp']}] {rec['year']} {rec['school']} / {rec['interview_type']} / {rec['criteria']}"
                ):
                    st.markdown("**질문**")
                    st.write(rec["question"])
                    st.markdown("**나의 답변**")
                    st.write(rec["user_answer"])
                    st.caption(f"세션: {rec['session_name']} · 모드: {rec['mode']}")

    with tab2:
        for i, rec in enumerate(reversed(all_logs), start=1):
            with st.expander(
                f"{i}. [{rec['timestamp']}] {rec['year']} {rec['school']} / {rec['interview_type']} / {rec['criteria']}"
            ):
                st.markdown("**질문**")
                st.write(rec["question"])
                st.markdown("**나의 답변**")
                st.write(rec["user_answer"])
                st.caption(
                    f"세션: {rec['session_name']} · 모드: {rec['mode']} · "
                    f"{'오답노트에 저장됨' if rec['marked_wrong'] else '오답노트 미저장'}"
                )


if __name__ == "__main__":
    main()
