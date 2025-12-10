# pages/4_MMI_Mode.py

import random
import streamlit as st

from config import DEFAULT_MMI_STATIONS, DEFAULT_MMI_TIME_PER_STATION_MIN
from services.question_loader import load_questions, filter_questions, get_question_by_index
from services.practice_log import init_practice_state, add_practice_record
from components.layout import render_page_header
from components.question_viewer import show_question_block


def _init_mmi_session():
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

    render_page_header("실전 MMI 모드", "여러 스테이션을 연속으로 풀며 실전처럼 연습합니다.")

    sess = st.session_state.mmi_session

    with st.sidebar:
        st.subheader("⚙️ 세션 설정")

        session_name = st.text_input("세션 이름", value=sess.get("session_name") or "오늘의 MMI 연습")
        num_stations = st.selectbox("스테이션 개수", [2, 3, 4, 6, 8], index=2)
        time_per_station = st.selectbox(
            "스테이션당 시간(분)", [5, 7, 10], index=1
        )

        years = ["전체"] + sorted({str(y) for y in df["year"].unique()})
        year_sel = st.selectbox("연도 필터", years)

        if st.button("🟢 세션 시작 / 재시작"):
            # 필터에 맞는 문제들 중에서 랜덤으로 num_stations개 선택
            filtered = filter_questions(df, year=year_sel)
            if filtered.empty:
                st.error("선택된 조건에 맞는 문제가 없습니다. 조건을 바꾸고 다시 시도하세요.")
            else:
                available_indices = list(filtered.index)
                if len(available_indices) <= num_stations:
                    chosen = available_indices
                else:
                    chosen = random.sample(available_indices, num_stations)

                st.session_state.mmi_session = {
                    "active": True,
                    "questions_idx": chosen,
                    "current_step": 0,
                    "session_name": session_name,
                    "time_per_station": time_per_station,
                    "filtered_year": year_sel,
                }
                st.success("새 MMI 세션이 시작되었습니다!")

    sess = st.session_state.mmi_session  # 업데이트

    if not sess["active"]:
        st.info("왼쪽 사이드바에서 세션을 설정한 뒤 **세션 시작** 버튼을 눌러주세요.")
        return

    # 현재 스테이션 정보
    questions_idx = sess["questions_idx"]
    current_step = sess["current_step"]
    total_steps = len(questions_idx)

    if current_step >= total_steps:
        st.success("🎉 모든 스테이션을 완료했습니다! 오답노트 페이지에서 기록을 복습해 보세요.")
        if st.button("다시 세션 설정하기"):
            st.session_state.mmi_session["active"] = False
        return

    st.markdown(f"### 스테이션 {current_step + 1} / {total_steps}")
    st.caption(f"세션 이름: {sess['session_name']}  ·  시간: {sess['time_per_station']}분")

    # 해당 인덱스의 문제 가져오기
    q_idx = questions_idx[current_step]
    question_row = df.loc[q_idx]

    user_answer, marked_wrong = show_question_block(
        question_row=question_row,
        timer_minutes=sess["time_per_station"],
        answer_key=f"mmi_answer_{current_step}",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 이 스테이션 기록 저장 후 다음으로 이동"):
            add_practice_record(
                question_row=question_row,
                user_answer=user_answer,
                mode="실전MMI",
                marked_wrong=marked_wrong,
                session_name=sess["session_name"],
            )
            st.session_state.mmi_session["current_step"] += 1
            st.experimental_rerun()
    with col2:
        if st.button("⏭ 이번 스테이션 건너뛰기"):
            st.session_state.mmi_session["current_step"] += 1
            st.experimental_rerun()


if __name__ == "__main__":
    main()
