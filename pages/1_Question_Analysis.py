# pages/1_Question_Analysis.py

import streamlit as st

from services.question_loader import load_questions, filter_questions
from services.practice_log import init_practice_state
from components.layout import render_page_header


def main():
    init_practice_state()
    df = load_questions()

    render_page_header("기출문제 분석", "연도·대학·유형별로 기출 문항 분포를 살펴봅니다.")

    with st.sidebar:
        st.subheader("🔍 필터")

        years = ["전체"] + sorted({str(y) for y in df["year"].unique()})
        schools = ["전체"] + sorted(df["school"].astype(str).unique())
        interview_types = ["전체"] + sorted(df["interview_type"].astype(str).unique())
        criteria_list = ["전체"] + sorted(df["criteria"].astype(str).unique())

        year_sel = st.selectbox("연도", years)
        school_sel = st.selectbox("대학", schools)
        itype_sel = st.selectbox("면접유형", interview_types)
        crit_sel = st.selectbox("평가요소", criteria_list)

    filtered = filter_questions(
        df,
        year=year_sel,
        school=school_sel,
        interview_type=itype_sel,
        criteria=crit_sel,
    )

    st.markdown("### 필터 결과 요약")
    st.write(f"조건에 맞는 문항 수: **{len(filtered)}** / 전체 {len(df)}문항")

    if filtered.empty:
        st.warning("조건에 맞는 문항이 없습니다. 필터를 조정해 보세요.")
        return

    # 평가요소 분포
    st.markdown("#### 📊 평가요소 분포")
    crit_counts = (
        filtered["criteria"].value_counts().rename_axis("criteria").reset_index(name="count")
    )
    st.bar_chart(crit_counts.set_index("criteria"))

    # 대학별 문항 수
    st.markdown("#### 🏫 대학별 문항 수")
    school_counts = (
        filtered["school"].value_counts().rename_axis("school").reset_index(name="count")
    )
    st.bar_chart(school_counts.set_index("school"))

    # 일부 문항 미리보기
    st.markdown("#### 🔎 샘플 문항 미리보기")
    for i, (_, row) in enumerate(filtered.head(5).iterrows(), start=1):
        with st.expander(f"{i}. {row['year']} {row['school']} / {row['interview_type']} / {row['criteria']}"):
            st.write(row["question"])

    st.info(
        "👉 이 분석을 바탕으로, 상단 메뉴에서 **문제 연습** 페이지로 이동해 "
        "해당 유형의 문제를 직접 풀어보세요."
    )


if __name__ == "__main__":
    main()
