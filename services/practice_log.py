# services/practice_log.py

from datetime import datetime
import streamlit as st


def init_practice_state():
    """
    세션 상태에 로그/오답노트 저장용 구조 초기화.
    """
    if "practice_logs" not in st.session_state:
        st.session_state.practice_logs = []  # 리스트[dict]
    if "practice_index" not in st.session_state:
        st.session_state.practice_index = 0
    if "mmi_session" not in st.session_state:
        st.session_state.mmi_session = {
            "active": False,
            "questions_idx": [],
            "current_step": 0,
            "session_name": "",
            "time_per_station": 7,
        }


def add_practice_record(
    question_row,
    user_answer: str,
    mode: str = "일반 연습",
    marked_wrong: bool = False,
    session_name: str | None = None,
):
    """
    한 번의 연습 결과(문항 + 나의 답변)를 practice_logs에 추가.
    """
    if question_row is None:
        return

    init_practice_state()

    # pandas Series -> dict
    qr = question_row.to_dict()

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mode": mode,
        "session_name": session_name or "",
        "year": str(qr.get("year", "")),
        "school": qr.get("school", ""),
        "interview_type": qr.get("interview_type", ""),
        "criteria": qr.get("criteria", ""),
        "question": qr.get("question", ""),
        "user_answer": user_answer,
        "marked_wrong": marked_wrong,
    }

    st.session_state.practice_logs.append(record)


def get_all_logs():
    init_practice_state()
    return st.session_state.practice_logs


def get_wrong_logs():
    init_practice_state()
    return [r for r in st.session_state.practice_logs if r.get("marked_wrong")]
