# services/strategy_loader.py

import pandas as pd


def load_strategies() -> pd.DataFrame:
    """
    대비 전략을 간단한 테이블로 제공.
    나중에 CSV나 DB로 빼고 싶으면 이 부분만 교체하면 됨.
    """
    data = [
        {
            "id": "ethics_4step",
            "category": "윤리 딜레마",
            "title": "윤리 딜레마 접근 4단계",
            "summary": "사실 파악 → 이해관계자 파악 → 원칙 적용 → 결론 및 대안 제시",
            "structure": "서론: 상황 요약 / 본론1: 이해관계자·가치 / 본론2: 선택지 비교 / 결론: 나의 입장 + 근거",
            "tips": "한쪽 편만 들지 말고, 최소 두 입장을 공정하게 다룬 뒤 본인의 입장을 정리하기.",
        },
        {
            "id": "communication_spike",
            "category": "의사소통",
            "title": "환자와의 어려운 대화(SPIKES 모델 응용)",
            "summary": "환경 조성 → 현재 상황 파악 → 정보 전달 → 감정 공감 → 함께 계획 세우기",
            "structure": "서론: 환자의 입장에서 상황 정리 / 본론: 공감 표현 + 정보 정리 / 결론: 함께 선택할 수 있는 다음 단계 제안",
            "tips": "‘~하시겠습니까?’ 보다 ‘함께 ~해보는 건 어떨까요?’ 같은 공동 결정을 강조.",
        },
        {
            "id": "mmi_basic_frame",
            "category": "공통",
            "title": "MMI 기본 답변 구조",
            "summary": "문제 재정리 → 가치/원칙 언급 → 구체적인 행동 계획 → 마무리 한 줄",
            "structure": "서론: 질문을 내 언어로 다시 말하기 / 본론: 기준·원칙·예시 / 결론: 한 문장으로 정리",
            "tips": "시간이 부족해도 ‘결론 한 줄’을 꼭 말해서 인상을 남기기.",
        },
        {
            "id": "teamwork_conflict",
            "category": "상황판단/팀워크",
            "title": "팀 내 갈등 상황 정리법",
            "summary": "사실과 감정을 분리 → 각 입장의 합리적 부분 찾기 → 공통 목표로 재정렬",
            "structure": "서론: 갈등 상황을 중립적으로 묘사 / 본론: 각자 입장 인정 + 공통 목표 / 결론: 합의 가능한 행동 제안",
            "tips": "누가 잘못했는지보다 팀의 공통 목표를 자주 언급하기.",
        },
        {
            "id": "self_intro_story",
            "category": "자기소개",
            "title": "스토리형 자기소개 틀",
            "summary": "한 문장 정체성 → 구체 사례 1~2개 → 의사가 되고 싶은 이유 연결",
            "structure": "서론: 나를 한 문장으로 / 본론: 경험·사례 / 결론: 앞으로의 목표와 연결",
            "tips": "너무 많은 활동 나열 말고, 한두 개 사례를 깊게 설명하기.",
        },
    ]
    return pd.DataFrame(data)
