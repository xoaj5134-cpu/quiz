# components/stats_cards.py

import streamlit as st


def show_overall_stats(practice_logs: list, total_questions: int):
    """
    홈/대시보드에서 보여줄 간단한 통계 카드.
    """
    total_solved = len(practice_logs)
    wrong_count = len([l for l in practice_logs if l.get("marked_wrong")])
    unique_questions = len({l.get("question") for l in practice_logs}) if practice_logs else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("총 문항 수(데이터 기준)", total_questions)
    with col2:
        st.metric("연습한 기록 수", total_solved)
    with col3:
        st.metric("연습한 서로 다른 문항 수", unique_questions)
    with col4:
        st.metric("오답노트에 저장된 문항 수", wrong_count)
