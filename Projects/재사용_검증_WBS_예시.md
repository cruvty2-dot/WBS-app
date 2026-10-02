# 재사용 진단 검증 프로젝트 WBS 예시

> 실제로 시작된 연구 프로젝트가 아닌 구조 예시다. 재사용 가능 여부를 판정할 기준을 검증하는 범위를 가정한다.

| WBS ID | 상위 | 작업·산출물 | 완료 기준 |
| --- | --- | --- | --- |
| demo.reuse |  | 재사용 진단 기준 검증 보고서 | 범위·데이터·검증·한계가 추적 가능한 보고서 |
| demo.reuse.scope | demo.reuse | 적용 대상·요구조건 명세 | 셀/모듈/팩 수준, 용도, 성능·안전 조건 정의 |
| demo.reuse.data | demo.reuse | 입력 데이터·이력 목록 | 단위·시료·SOC·온도·측정조건·출처 연결 |
| demo.reuse.method | demo.reuse | 진단·분석 절차서 | 용량·저항·EIS 등 지표의 적용 근거와 검증 절차 |
| demo.reuse.validation | demo.reuse | 검증 결과·오류 분석 | 독립 검증 자료와 판정 오류·적용 제한 확인 |
| demo.reuse.report | demo.reuse | 검토된 최종 보고서 | 결과·기준·범위·추가 과제의 검토 완료 |

각 작업은 지식 분류 `p.recycle.diagnose`, `method.eis`, `d.eval.degradation` 등과 연결한다. 지식 트리의 모든 항목을 프로젝트에 복사하지 않는다. 실제 프로젝트에서는 범위의 100%를 하위 작업이 포괄하도록 조정하고 중복 산출물을 제거한다.
