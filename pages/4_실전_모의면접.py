# pages/4_실전_모의면접.py

import random
import streamlit as st

from config import DEFAULT_MMI_STATIONS, DEFAULT_MMI_TIME_PER_STATION_MIN
from services.question_loader import load_questions, filter_questions
from services.practice_log import init_practice_state, add_practice_record
from components.layout import render_page_header
from components.question_viewer import show_question_block


def _init_mmi_session():
    """실전 모의면접 세션용 상태 초기화 (변수 이름은 그대로 mmi_session 사용)."""
    if "mmi_session" not in st.session_state:
        st.session_state.mmi_session = {
            "active": False,
            "questions_idx": [],
            "current_step": 0,
            "session_name": "",
            "time_per_station": DEFAULT_MMI_TIME_PER_STATION_MIN,
        }


def main():
    init_practice_state()
    _init_mmi_session()
    df = load_questions()

    # 페이지 상단 제목
    render_page_header(
        "실전 모의면접 모드",
        "여러 문항을 연속으로 풀며 실전처럼 연습합니다.",
    )

    sess = st.session_state.mmi_session

    # ----- 사이드바: 세션 설정 -----
    with st.sidebar:
        st.subheader("⚙️ 세션 설정")

        session_name = st.text_input(
            "세션 이름",
            value=sess.get("session_name") or "오늘의 모의면접 연습",
        )

        num_questions = st.selectbox(
            "문항 개수",
            [2, 3, 4, 6, 8],
            index=2,  # 기본 4문항
        )

        time_per_question = st.selectbox(
            "문항당 시간(분)",
            [5, 7, 10],
            index=1,  # 기본 7분
        )

        years = ["전체"] + sorted({str(y) for y in df["year"].unique()})
        year_sel = st.selectbox("연도 필터", years)

        if st.button("🟢 세션 시작 / 재시작"):
            # 필터에 맞는 문제들 중에서 랜덤으로 num_questions개 선택
            filtered = filter_questions(df, year=year_sel)
            if filtered.empty:
                st.error(
                    "선택된 조건에 맞는 문제가 없습니다.\n"
                    "연도 필터를 바꾸거나 Question Analysis 페이지에서 데이터 분포를 먼저 확인해 보세요."
                )
            else:
                available_indices = list(filtered.index)
                if len(available_indices) <= num_questions:
                    chosen = available_indices
                else:
                    chosen = random.sample(available_indices, num_questions)

                st.session_state.mmi_session = {
                    "active": True,
                    "questions_idx": chosen,
                    "current_step": 0,
                    "session_name": session_name,
                    "time_per_station": time_per_question,
                    "filtered_year": year_sel,
                }
                st.success("새 실전 모의면접 세션이 시작되었습니다!")

    # 업데이트된 세션 다시 가져오기
    sess = st.session_state.mmi_session

    # ----- 아직 세션이 없으면 안내 -----
    if not sess["active"]:
        st.info(
            "왼쪽 사이드바에서 **세션 이름 / 문항 개수 / 시간 / 연도**를 설정한 뒤 "
            "**[세션 시작 / 재시작]** 버튼을 눌러 주세요."
        )
        return

    questions_idx = sess["questions_idx"]
    current_step = sess["current_step"]
    total_steps = len(questions_idx)

    # ----- 모든 문항 완료 -----
    if current_step >= total_steps:
        st.success(
            "🎉 모든 문항을 완료했습니다!\n\n"
            "오답노트 / 연습 기록 페이지에서 오늘 연습한 내용을 복습해 보세요."
        )
        if st.button("새 세션 설정하기"):
            st.session_state.mmi_session["active"] = False
        return

    # ----- 현재 문항 정보 표시 -----
    st.markdown(f"### 문항 {current_step + 1} / {total_steps}")
    st.caption(
        f"세션 이름: {sess['session_name']}  ·  "
        f"문항당 시간: {sess['time_per_station']}분"
    )

    # 해당 인덱스의 문제 가져오기
    q_idx = questions_idx[current_step]
    question_row = df.loc[q_idx]

    # 문항 표시 + 답변 입력 UI
    user_answer, marked_wrong = show_question_block(
        question_row=question_row,
        timer_minutes=sess["time_per_station"],
        answer_key=f"mock_interview_answer_{current_step}",
    )

    # ----- 버튼: 기록 저장 / 건너뛰기 -----
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ 이 문항 기록 저장 후 다음으로 이동"):
            add_practice_record(
                question_row=question_row,
                user_answer=user_answer,
                mode="실전 모의면접",
                marked_wrong=marked_wrong,
                session_name=sess["session_name"],
            )
            st.session_state.mmi_session["current_step"] += 1
            st.experimental_rerun()

    with col2:
        if st.button("⏭ 이 문항 건너뛰기"):
            st.session_state.mmi_session["current_step"] += 1
            st.experimental_rerun()


if __name__ == "__main__":
    main()
