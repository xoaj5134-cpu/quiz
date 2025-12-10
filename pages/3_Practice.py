# pages/3_Practice.py

import streamlit as st

from services.question_loader import load_questions, filter_questions, get_random_question, get_question_by_index
from services.practice_log import init_practice_state, add_practice_record
from components.layout import render_page_header
from components.question_viewer import show_question_block


def main():
    init_practice_state()
    df = load_questions()

    render_page_header("문제 연습", "기출/예상 문제를 선택해서 답변을 연습합니다.")

    with st.sidebar:
        st.subheader("🎯 연습 설정")

        mode = st.selectbox(
            "문제 출처(모드)",
            ["전체", "기출(quiz.csv)", "예상(추가 예정)"],
        )

        years = ["전체"] + sorted({str(y) for y in df["year"].unique()})
        schools = ["전체"] + sorted(df["school"].astype(str).unique())
        criteria_list = ["전체"] + sorted(df["criteria"].astype(str).unique())

        year_sel = st.selectbox("연도", years)
        school_sel = st.selectbox("대학", schools)
        crit_sel = st.selectbox("평가요소", criteria_list)

        order_mode = st.radio("문항 선택 방식", ["랜덤", "순서대로"])

        timer_min = st.selectbox("타이머(분)", [3, 5, 7, 10], index=1)

    # 예상 모드는 아직 데이터 없으니 안내
    source_filter = None
    if mode.startswith("기출"):
        source_filter = "기출"
    elif mode.startswith("예상"):
        st.warning("예상 문제 데이터는 아직 CSV에 포함되어 있지 않습니다. 현재는 기출만 연습 가능합니다.")
        source_filter = None  # 실제로는 전체 중에서만 필터

    filtered = filter_questions(
        df,
        year=year_sel,
        school=school_sel,
        criteria=crit_sel,
        source=source_filter,
    )

    if filtered.empty:
        st.warning("조건에 맞는 문항이 없습니다. 필터를 조정해 보세요.")
        return

    # 순서대로 모드일 때 사용할 인덱스 관리
    if order_mode == "순서대로":
        if "practice_index" not in st.session_state:
            st.session_state.practice_index = 0

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("⬅ 이전 문제"):
                st.session_state.practice_index -= 1
        with col_btn2:
            if st.button("다음 문제 ➡"):
                st.session_state.practice_index += 1

        question = get_question_by_index(filtered, st.session_state.practice_index)
    else:
        # 랜덤
        if st.button("🔄 새 랜덤 문제 뽑기"):
            # 버튼 클릭 시에만 새로운 문제 샘플링
            st.session_state.current_random_question = get_random_question(filtered)

        if "current_random_question" not in st.session_state:
            st.session_state.current_random_question = get_random_question(filtered)

        question = st.session_state.current_random_question

    # 실제 문제 보여주기
    user_answer, marked_wrong = show_question_block(
        question_row=question,
        timer_minutes=timer_min,
        answer_key="practice_answer",
    )

    if st.button("✅ 이 연습 기록 저장하기"):
        add_practice_record(
            question_row=question,
            user_answer=user_answer,
            mode=f"문제연습/{order_mode}",
            marked_wrong=marked_wrong,
            session_name="단일 연습",
        )
        st.success("연습 기록이 저장되었습니다. 오답노트 페이지에서 다시 볼 수 있습니다.")


if __name__ == "__main__":
    main()
