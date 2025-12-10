# app.py

import streamlit as st

from config import APP_TITLE, APP_DESCRIPTION
from services.question_loader import load_questions
from services.practice_log import init_practice_state, get_all_logs
from components.layout import render_page_header
from components.stats_cards import show_overall_stats


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🩺",
    layout="wide",
)


def main():
    init_practice_state()
    df = load_questions()
    logs = get_all_logs()

    render_page_header(APP_TITLE, APP_DESCRIPTION)

    show_overall_stats(logs, total_questions=len(df))

    st.markdown("### 오늘은 어떻게 연습할까요?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 1. 기출문제 분석")
        st.write("연도·대학·유형별 기출 문항 분포를 보고 출제 경향을 파악해요.")
        st.caption("상단 좌측 페이지 메뉴에서 **기출문제 분석** 페이지를 선택하세요.")

    with col2:
        st.markdown("#### 2. 전략 정리 & 문제 연습")
        st.write("대비 전략을 카드로 정리하고, 문제를 골라 답변을 작성해요.")
        st.caption("**대비전략**, **문제 연습** 페이지를 차례대로 연습해 보세요.")

    with col3:
        st.markdown("#### 3. 실전 MMI 모드")
        st.write("여러 스테이션을 연달아 풀며 실전처럼 연습하고 오답노트에 남길 수 있어요.")
        st.caption("**실전 MMI 모드**, **오답노트** 페이지에서 복습까지!")

    st.markdown("---")
    st.markdown(
        """
        **사용 팁**
        - 왼쪽 상단의 ☰ 메뉴에서 각 페이지(기출분석 / 대비전략 / 문제연습 / 실전 MMI / 오답노트)를 이동할 수 있어요.  
        - 한 번 연습을 마칠 때마다, `오답노트에 저장` 체크 후 `기록 저장` 버튼을 눌러 주세요.
        """
    )


if __name__ == "__main__":
    main()
