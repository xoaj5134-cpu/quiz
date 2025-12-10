# components/question_viewer.py

import time
from datetime import datetime
import streamlit as st


def render_countdown_timer(key_prefix: str, minutes: int = 5):
    """
    아주 간단한 카운트다운 타이머.
    - '타이머 시작' 버튼을 누르면 종료 시각을 session_state에 저장
    - 페이지가 다시 실행될 때마다 남은 시간을 계산해서 표시
    (자동으로 1초마다 새로고침되지는 않고, 상호작용 시 갱신되는 형태)
    """
    end_key = f"{key_prefix}_end_time"

    col_t1, col_t2 = st.columns([1, 2])

    with col_t1:
        if st.button("⏱ 타이머 시작", key=f"{key_prefix}_start"):
            st.session_state[end_key] = time.time() + minutes * 60

    with col_t2:
        if end_key in st.session_state:
            remaining = st.session_state[end_key] - time.time()
            if remaining > 0:
                m = int(remaining // 60)
                s = int(remaining % 60)
                st.info(f"남은 시간: {m}분 {s}초 (페이지가 다시 실행될 때 갱신됩니다)")
            else:
                st.warning("⏰ 시간 종료!")


def show_question_block(question_row, timer_minutes: int = 5, answer_key: str = "user_answer"):
    """
    하나의 문제를 보여주고, 답변 입력 + 오답노트 체크 + 모범답안 토글까지 포함한 블록.

    반환값:
        user_answer(str), marked_wrong(bool)
    """
    if question_row is None:
        st.warning("표시할 문제가 없습니다.")
        return "", False

    st.subheader("📌 면접 문항")

    # 메타 정보
    meta_cols = st.columns(4)
    with meta_cols[0]:
        st.caption(f"연도: {question_row.get('year', '')}")
    with meta_cols[1]:
        st.caption(f"대학: {question_row.get('school', '')}")
    with meta_cols[2]:
        st.caption(f"면접유형: {question_row.get('interview_type', '')}")
    with meta_cols[3]:
        st.caption(f"평가요소: {question_row.get('criteria', '')}")

    st.write(question_row.get("question", ""))

    st.markdown("---")

    # 타이머
    st.markdown("#### ⏱ 준비 타이머")
    render_countdown_timer("practice_timer", minutes=timer_minutes)

    st.markdown("#### ✏️ 나의 답변")
    user_answer = st.text_area(
        "여기에 답변을 정리해 보세요.",
        key=answer_key,
        height=200,
    )

    col1, col2 = st.columns(2)
    with col1:
        marked_wrong = st.checkbox("이 문항을 오답노트에 저장하기", key=f"{answer_key}_wrong")
    with col2:
        show_sample = st.checkbox("모범 답안 / 해설 보기 (데이터가 있을 경우)", key=f"{answer_key}_show_sample")

    if show_sample:
        st.markdown("#### 📖 모범 답안 / 해설")
        # question_row에 sample_answer 컬럼이 있다면 표시, 없으면 안내 문구
        sample = question_row.get("sample_answer", None)
        if sample and isinstance(sample, str) and sample.strip():
            st.write(sample)
        else:
            st.info(
                "아직 모범답안 데이터가 없습니다.\n\n"
                "• PDF나 별도 자료를 보면서 스스로 모범답안을 만들어보고,\n"
                "• 나중에 CSV에 sample_answer 컬럼을 추가해 넣어도 좋아요."
            )

    return user_answer, marked_wrong
