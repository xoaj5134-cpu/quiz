# services/question_loader.py

import pandas as pd
from config import QUIZ_CSV_PATH


def _load_raw_quiz(path: str = QUIZ_CSV_PATH) -> pd.DataFrame:
    """
    quiz.csv를 읽어서 원본 DataFrame을 반환.
    기본적으로 cp949(엑셀 한글)로 시도 후 실패 시 utf-8 계열로 재시도.
    """
    try:
        df = pd.read_csv(path, encoding="cp949")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding="utf-8-sig")
        except UnicodeDecodeError:
            df = pd.read_csv(path)  # 마지막 fallback
    return df


def _normalize_quiz_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    한글 컬럼명을 영어 컬럼명으로 통일하고, 필요하면 기본 컬럼(source, difficulty 등)을 추가.
    현재 quiz.csv 헤더 예시:
    연도,지역,대학명,전형 ,학과,면접유형,평가요소,면접문항
    """
    # 공백 제거
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    rename_map = {
        "연도": "year",
        "지역": "region",
        "대학명": "school",
        "전형": "track",
        "학과": "major",
        "면접유형": "interview_type",
        "평가요소": "criteria",
        "면접문항": "question",
    }

    df = df.rename(columns=rename_map)

    # source(기출/예상) 컬럼이 없다면 기본값으로 기출 처리
    if "source" not in df.columns:
        df["source"] = "기출"

    # difficulty 컬럼 없으면 빈 값으로
    if "difficulty" not in df.columns:
        df["difficulty"] = ""

    return df


def load_questions(path: str = QUIZ_CSV_PATH) -> pd.DataFrame:
    """
    앱에서 사용할 통합 questions DataFrame 반환.
    """
    df = _load_raw_quiz(path)
    df = _normalize_quiz_df(df)
    return df


def filter_questions(
    df: pd.DataFrame,
    year: str | None = None,
    school: str | None = None,
    interview_type: str | None = None,
    criteria: str | None = None,
    source: str | None = None,
) -> pd.DataFrame:
    """
    주어진 조건들로 DataFrame 필터링.
    None이면 해당 조건은 무시.
    """
    q = df.copy()

    if year and year != "전체":
        q = q[q["year"].astype(str) == str(year)]

    if school and school != "전체":
        q = q[q["school"] == school]

    if interview_type and interview_type != "전체":
        q = q[q["interview_type"] == interview_type]

    if criteria and criteria != "전체":
        q = q[q["criteria"] == criteria]

    if source and source != "전체" and "source" in q.columns:
        q = q[q["source"] == source]

    return q


def get_random_question(df: pd.DataFrame):
    """
    DataFrame에서 랜덤으로 한 문제 반환 (Series).
    """
    if df.empty:
        return None
    return df.sample(1).iloc[0]


def get_question_by_index(df: pd.DataFrame, index: int):
    """
    순서대로 보기 모드를 위해, 인덱스로 문제 하나 가져오기.
    df가 비어있으면 None.
    """
    if df.empty:
        return None
    index = index % len(df)
    return df.iloc[index]
