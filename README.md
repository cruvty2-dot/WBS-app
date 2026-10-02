# 배터리 공부

이차전지의 소재·설계·평가·제조공정 자료를 **설계 / 공정** 두 축으로 정리한다. 아래 WBS 목차에서 항목을 찾고 연결된 설명과 PDF를 연다.

- 최상위 학습자료: **이차전지**
- 현재 자료: 전체 분류안, 주제별 PDF 14개, Markdown 학습자료, Li 상세 예시
- 현재 단계: 자료·분류 구성 완료. 탐색 웹앱과 Hermes 실제 연결은 후속 구현.

## 목차

| 문서·목차 | 역할 |
| --- | --- |
| [전체 WBS 목차](#전체-wbs-목차) | 모든 학습 항목의 번호·계층·연결 자료 |
| [1. 설계](#1-설계) | 소재·재료, 전극, 셀·시스템, 평가·분석·열화, 차세대전지 |
| [2. 공정](#2-공정) | 원료·소재 제조, 전극 제조, 조립, 화성·숙성, 품질, 재사용·재활용, 공급망 |
| [주제별 PDF](#주제별-pdf) | 학습자료 14개의 설명·PDF·쪽수 |
| [분류·기준·근거](#분류기준근거) | 세부 분류 원칙, 소재와 원소의 관계, 표준, 원본 쪽수 |
| [아이디어·프로젝트·기록 양식](#아이디어프로젝트기록-양식) | 아이디어를 작업으로 나누고 분석 기록·요청을 작성 |
| [운영·연동 계획](#운영연동-계획) | 수정·저장 규칙, 요구사항, GPT·GitHub·Hermes 연결 계획 |
| [사용 방법](#사용-방법) | 이 목차를 찾고 자료를 보완하는 방법 |

## 전체 WBS 목차

WBS(항목을 계층적으로 나누는 구조) 번호는 학습자료의 위치를 찾는 번호이며 학습 순서나 진도를 뜻하지 않는다. 현재 분류안의 최상위 이차전지 아래 **195개 항목을 모두 펼쳤다**. 프로젝트의 실제 작업 WBS는 아래 별도 예시를 참고한다.

연결 문서는 현재 확보한 **주제별 공통 학습자료**다. 여러 세부 항목이 같은 자료를 참조할 수 있으며, 각 항목의 전용 상세 문서는 이후 보완한다. Li는 공통 상세 문서로 연결한다.

## 1. 설계

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 1 | **설계** | [내용](Knowledge/topics/00_guide.md) · [PDF](References/topics/00_학습지도·용어·공식.pdf) |

### 1.1 소재·재료

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 1.1 | **소재·재료** | [소재 분류](Docs/양극재_분류와_구성원소.md) / [소재 기초](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1 | **소재 특성·전공 기초** | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1 | **원소·이온** | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.1 | Li: 원소·Li⁺·금속 음극 | [내용](Knowledge/materials/Li.md) · [PDF](References/topics/13_Li_리튬.pdf) |
| 1.1.1.1.2 | Ni: 니켈 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.3 | Co: 코발트 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.4 | Mn: 망간 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.5 | Fe: 철 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.6 | P: 인 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.7 | C: 탄소 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.8 | Si: 규소 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.9 | Al: 알루미늄 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.10 | Cu: 구리 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.11 | O: 산소 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.1.12 | Na: 나트륨 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.2 | **결정구조·결함** | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.2.1 | 층상 구조 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.2.2 | 올리빈 구조 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.2.3 | 스피넬 구조 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.2.4 | 공공·자리 혼입·입계 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.2.5 | 상전이·응력·균열 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.3 | **전자구조·결합** | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.3.1 | 화학결합·산화수 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.3.2 | 오비탈·밴드·전자상태 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.3.3 | 산화·환원과 전위 | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) |
| 1.1.1.4 | **전달·반응·열 특성** | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) |
| 1.1.1.4.1 | 확산·이온 전달 | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) |
| 1.1.1.4.2 | 전자 전달 | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) |
| 1.1.1.4.3 | 열전달·열 안정성 | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) |
| 1.1.1.4.4 | 계면 반응·젖음성 | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) |
| 1.1.1.5 | **입자·분체·표면** | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.5.1 | 입도·입도분포 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.5.2 | 비표면적·표면화학 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.1.5.3 | 진밀도·탭밀도·충전성 | [내용](Knowledge/topics/01_material-basics.md) · [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) |
| 1.1.2 | **활물질** | [양극재](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) / [음극재](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.1 | **양극재** | [내용](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.1 | **층상 산화물** | [내용](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.1.1 | NCM | [소재 분류](Docs/양극재_분류와_구성원소.md) / [양극재](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.1.2 | NCA | [소재 분류](Docs/양극재_분류와_구성원소.md) / [양극재](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.1.3 | LCO | [소재 분류](Docs/양극재_분류와_구성원소.md) / [양극재](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.2 | **인산염계** | [내용](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.2.1 | LFP | [소재 분류](Docs/양극재_분류와_구성원소.md) / [양극재](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.2.2 | LMFP | [소재 분류](Docs/양극재_분류와_구성원소.md) / [양극재](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.3 | **스피넬계** | [내용](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.3.1 | LMO | [소재 분류](Docs/양극재_분류와_구성원소.md) / [양극재](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.3.2 | LNMO | [내용](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.4 | **황·전환반응계** | [내용](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.1.4.1 | 황 양극 | [내용](Knowledge/topics/03_cathodes.md) · [PDF](References/topics/03_양극재·반응·열화.pdf) |
| 1.1.2.2 | **음극재** | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.1 | **탄소계** | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.1.1 | **흑연** | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.1.1.1 | 천연흑연 | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.1.1.2 | 인조흑연 | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.1.2 | 하드카본 | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.2 | **Si계·합금계** | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.2.1 | Si | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.2.2 | SiOₓ | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.2.3 | Si-C 복합체 | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.3 | **삽입형 산화물** | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.3.1 | LTO | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.4 | **금속 음극** | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.2.2.4.1 | 리튬 금속 음극 | [Li 상세](Knowledge/materials/Li.md) · [PDF](References/topics/13_Li_리튬.pdf) / [음극재](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.1.3 | **바인더** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.3.1 | PVDF | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.3.2 | CMC | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.3.3 | SBR | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.3.4 | PAA | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.3.5 | PTFE | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.4 | **도전재** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.4.1 | 카본블랙 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.4.2 | CNT | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.4.3 | 그래핀 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5 | **전해질** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.1 | **액체 전해질** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.1.1 | **리튬염** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.1.1.1 | LiPF₆ | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.1.1.2 | LiFSI | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.1.1.3 | LiTFSI | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.1.2 | 용매 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.1.3 | 첨가제 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.2 | **고체 전해질** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.2.1 | 황화물계 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.2.2 | 산화물계 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.2.3 | 고분자계 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.3 | 겔·고분자 전해질 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.5.4 | SEI·CEI 계면막 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.6 | **분리막** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.6.1 | PE·PP계 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.6.2 | 세라믹·기능성 코팅 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.7 | **집전체** | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.7.1 | Al 집전체 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.7.2 | Cu 집전체 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |
| 1.1.7.3 | 표면 처리·복합 집전체 | [내용](Knowledge/topics/05_electrolyte-and-additives.md) · [PDF](References/topics/05_전해질·바인더·보조소재.pdf) |

### 1.2 전극 설계

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 1.2 | **전극 설계** | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.2.1 | 조성·활물질 비율 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.2.2 | 로딩량·면적당 용량 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.2.3 | 두께·밀도·공극률 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.2.4 | 이온·전자 전달망 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.2.5 | N/P·리튬 재고 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.2.6 | 접착·계면·젖음 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |

### 1.3 셀·시스템 설계

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 1.3 | **셀·시스템 설계** | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.3.1 | 용도·요구 성능 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.3.2 | 원통형·각형·파우치 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.3.3 | 전압·SOC·온도 사용창 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.3.4 | 전해액량·압력 | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.3.5 | 모듈·팩·BMS | [내용](Knowledge/topics/06_electrode-and-cell-design.md) · [PDF](References/topics/06_전극·셀_설계_계산.pdf) |
| 1.3.6 | 분해·재사용을 고려한 설계 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |

### 1.4 평가·분석·열화

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 1.4 | **평가·분석·열화** | [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) / [열화·차세대](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.1 | **전기화학 평가** | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.1.1 | GCD·CC-CV | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.1.2 | C-rate·수명·쿨롱 효율 | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.1.3 | EIS | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.1.4 | CV·LSV | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.1.5 | GITT·PITT | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.1.6 | DCIR·HPPC | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.1.7 | dQ/dV·OCV·자가방전 | [내용](Knowledge/topics/02_electrochemistry.md) · [PDF](References/topics/02_전기화학_기초.pdf) / [평가·분석](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2 | **소재·전극 기기분석** | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2.1 | XRD | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2.2 | SEM·EDS·TEM | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2.3 | XPS·표면분석 | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2.4 | ICP-OES·ICP-MS | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2.5 | GC·HPLC·MS | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2.6 | PSA·BET·공극분석 | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.2.7 | DSC·TGA·ARC | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 1.4.3 | **열화·고장 분석** | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.3.1 | LLI: 순환 가능한 Li 감소 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.3.2 | LAM: 반응 가능한 활물질 감소 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.3.3 | 저항·분극 증가 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.3.4 | 리튬 석출·고립 | [내용](Knowledge/topics/04_anodes.md) · [PDF](References/topics/04_음극재·리튬_석출.pdf) |
| 1.4.3.5 | 전극 간 영향·용출 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.3.6 | 고장 원인과 기여 요인 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.4 | 안전·열 특성 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.4.5 | 국제·국내 표준 | [내용](Docs/이차전지_WBS_표준_지침.md) |

### 1.5 다화학계·차세대전지

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 1.5 | **다화학계·차세대전지** | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.5.1 | 전고체전지 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.5.2 | 나트륨이온전지 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.5.3 | 리튬황전지 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |
| 1.5.4 | 리튬 금속 전지 | [내용](Knowledge/topics/09_degradation-and-next-generation.md) · [PDF](References/topics/09_열화·안전·차세대전지.pdf) |

## 2. 공정

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2 | **공정** | [내용](Knowledge/topics/00_guide.md) · [PDF](References/topics/00_학습지도·용어·공식.pdf) |

### 2.1 원료·소재 제조

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2.1 | **원료·소재 제조** | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.1.1 | 입고·보관·수입검사 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.1.2 | 전구체·공침·결정화 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.1.3 | 리튬화·소성 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.1.4 | 분쇄·분급·도핑·코팅 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.1.5 | 흑연·Si계 소재 제조 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |

### 2.2 전극 제조

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2.2 | **전극 제조** | [습식·전극 제조](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) / [건식·품질](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.1 | **습식 전극** | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.1.1 | 계량·배합 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.1.2 | 혼합·분산 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.1.3 | 유변학·슬러리 안정성 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.1.4 | 여과·탈포·저장 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.1.5 | 도공 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.1.6 | 건조·용매 회수 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.2 | **건식 전극** | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.2.1 | 분체 혼합 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.2.2 | 바인더 섬유화 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.2.3 | 필름화·집전체 접합 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.3 | **압연·가공·최종 건조** | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.3.1 | 압연 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.3.2 | 슬리팅·노칭 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.3.3 | 진공 건조 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.3.4 | 전극 완제품 품질 | [내용](Knowledge/topics/10_electrode-manufacturing.md) · [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) |
| 2.2.4 | **스케일업·공정창** | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.4.1 | 교반·분산 스케일업 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.4.2 | 도공·건조 스케일업 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.2.4.3 | DOE: 실험계획법 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |

### 2.3 셀 조립

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2.3 | **셀 조립** | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.3.1 | 적층·권취 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.3.2 | 탭·용접 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.3.3 | 주액·함침 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.3.4 | 밀봉·누설검사 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.3.5 | 코인셀·하프셀 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |

### 2.4 화성·숙성·선별

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2.4 | **화성·숙성·선별** | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.4.1 | 초기 충전·계면막 형성 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.4.2 | 탈기 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.4.3 | 숙성·자가방전 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |
| 2.4.4 | 검사·등급 선별 | [내용](Knowledge/topics/07_assembly-and-formation.md) · [PDF](References/topics/07_셀_조립·함침·화성.pdf) |

### 2.5 품질·공정 데이터

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2.5 | **품질·공정 데이터** | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.5.1 | CTQ: 핵심 품질 특성 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.5.2 | SPC: 통계적 공정관리 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.5.3 | MSA: 측정시스템 분석 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.5.4 | 로트·설비·시료 추적 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |
| 2.5.5 | Python·MATLAB·분석 도구 | [내용](Knowledge/topics/08_evaluation-and-analysis.md) · [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) |
| 2.5.6 | 데이터·모델 검증 | [내용](Knowledge/topics/11_dry-electrode-and-quality.md) · [PDF](References/topics/11_건식전극·스케일업·품질.pdf) |

### 2.6 재사용·재활용

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2.6 | **재사용·재활용** | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.1 | 회수·이력·안전 상태 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.2 | 잔존성능·재사용 진단 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.3 | 재사용·재제조 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.4 | 분해·전처리 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.5 | 건식 제련 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.6 | 습식 제련 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.7 | 직접 재활용·재리튬화 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |
| 2.6.8 | 회수 소재의 품질 평가 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |

### 2.7 공급망·산업·직무

| WBS 번호 | 분류·학습 항목 | 연결 문서 |
| --- | --- | --- |
| 2.7 | 공급망·산업·직무 | [내용](Knowledge/topics/12_recycling-and-applications.md) · [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) |

## 주제별 PDF

원본의 본문·표·그래프를 보존하고 필요한 보완 설명을 앞에 추가했다. 원본과 새 PDF의 쪽수 관계는 [원본 자료 배치표](Docs/원본_자료_배치표.md)에서 확인한다.

| 자료 | Markdown | PDF | 쪽수 |
| --- | --- | --- | --- |
| 00. 학습지도·용어·공식 | [설명](Knowledge/topics/00_guide.md) | [PDF](References/topics/00_학습지도·용어·공식.pdf) | 10 |
| 01. 소재 특성·결정·전자구조 | [설명](Knowledge/topics/01_material-basics.md) | [PDF](References/topics/01_소재_특성·결정·전자구조.pdf) | 5 |
| 02. 전기화학 기초 | [설명](Knowledge/topics/02_electrochemistry.md) | [PDF](References/topics/02_전기화학_기초.pdf) | 7 |
| 03. 양극재·반응·열화 | [설명](Knowledge/topics/03_cathodes.md) | [PDF](References/topics/03_양극재·반응·열화.pdf) | 25 |
| 04. 음극재·리튬 석출 | [설명](Knowledge/topics/04_anodes.md) | [PDF](References/topics/04_음극재·리튬_석출.pdf) | 7 |
| 05. 전해질·바인더·보조소재 | [설명](Knowledge/topics/05_electrolyte-and-additives.md) | [PDF](References/topics/05_전해질·바인더·보조소재.pdf) | 6 |
| 06. 전극·셀 설계 계산 | [설명](Knowledge/topics/06_electrode-and-cell-design.md) | [PDF](References/topics/06_전극·셀_설계_계산.pdf) | 6 |
| 07. 셀 조립·함침·화성 | [설명](Knowledge/topics/07_assembly-and-formation.md) | [PDF](References/topics/07_셀_조립·함침·화성.pdf) | 5 |
| 08. 평가·기기분석·데이터 해석 | [설명](Knowledge/topics/08_evaluation-and-analysis.md) | [PDF](References/topics/08_평가·기기분석·데이터_해석.pdf) | 16 |
| 09. 열화·안전·차세대전지 | [설명](Knowledge/topics/09_degradation-and-next-generation.md) | [PDF](References/topics/09_열화·안전·차세대전지.pdf) | 9 |
| 10. 전극 제조·혼합·도공·건조·압연 | [설명](Knowledge/topics/10_electrode-manufacturing.md) | [PDF](References/topics/10_전극_제조·혼합·도공·건조·압연.pdf) | 15 |
| 11. 건식전극·스케일업·품질 | [설명](Knowledge/topics/11_dry-electrode-and-quality.md) | [PDF](References/topics/11_건식전극·스케일업·품질.pdf) | 8 |
| 12. 공급망·재사용·재활용·직무 | [설명](Knowledge/topics/12_recycling-and-applications.md) | [PDF](References/topics/12_공급망·재사용·재활용·직무.pdf) | 9 |
| 13. Li: 원소·이온·금속 음극 | [상세](Knowledge/materials/Li.md) | [PDF](References/topics/13_Li_리튬.pdf) | 2 |

## 분류·기준·근거

| 문서 | 역할 |
| --- | --- |
| [이차전지 지식 분류안](Docs/이차전지_지식분류안.md) | 설계·공정 계층과 공통 문서 연결 원칙 |
| [양극재 분류와 구성 원소](Docs/양극재_분류와_구성원소.md) | LFP·LMFP·NCM·LMO 등 소재 계열과 Li·Fe·Mn 등 원소의 관계 |
| [Li 상세](Knowledge/materials/Li.md) | 원소 Li, Li⁺, 리튬 금속 음극의 구분과 기본 특성 |
| [국제·국내 표준 및 전극 지침](Docs/이차전지_WBS_표준_지침.md) | WBS·전극 관련 표준의 적용 범위와 근거 |
| [원본 자료 배치표](Docs/원본_자료_배치표.md) | 원본의 어떤 쪽이 어느 주제 PDF에 포함됐는지 확인 |

## 아이디어·프로젝트·기록 양식

| 문서·양식 | 역할 |
| --- | --- |
| [재사용 아이디어](Knowledge/ideas/재사용_아이디어.md) | 메모의 질문·아이디어를 주제와 검증 과제로 정리 |
| [재사용 검증 프로젝트 WBS](Projects/재사용_검증_WBS_예시.md) | 지식 분류를 실제 작업·산출물로 연결하는 예시 |
| [작업 요청 양식](Templates/작업요청.md) | 목표·입력·작업 범위·완료 기준을 기록 |
| [분석 기록 양식](Templates/analysis-record.json) | 시료·조건·처리 이력·해석·검토 상태를 기록 |

## 운영·연동 계획

| 문서 | 역할 |
| --- | --- |
| [요구사항과 연동 계획](Docs/앱_요구사항과_연동계획.md) | 앱 기능과 GPT·GitHub·Hermes의 역할 |
| [저장 구조와 기록 규칙](Docs/저장_구조와_기록규칙.md) | 문서 위치·수정·검토·저장 범위 관리 |
| [작업 현황](Docs/작업_현황.md) | 완료한 자료와 앞으로 구현할 기능 |

## 사용 방법

1. 설계 또는 공정에서 공부할 항목을 찾는다.
2. 연결된 설명을 읽고 필요한 PDF를 연다.
3. 소재 설명에서 구성 원소·설계 변수·공정·분석법을 함께 확인한다.
4. 이 채팅에서 수정할 항목과 내용을 알려주면 관련 문서와 PDF를 갱신한다. 같은 경로의 최신본을 유지하고 이전 내용은 Git 변경 이력에 남긴다.
5. 새 항목이나 분류 변경이 생기면 전체 WBS 목차와 분류 데이터를 함께 맞춘다.

<details>
<summary>제작·검증 자료</summary>

- [분류 데이터](Data/taxonomy.json): 고유 ID, 탐색 계층, 관련 문서·원소 관계
- [주제별 자료 목록](Data/topic-manifest.json): 문서·PDF·원본 위치
- [원본 쪽수 대응 데이터](Data/source-page-map.json): 원본과 분리 PDF의 쪽수 대응

PDF 재생성에는 원본 2개와 Noto Sans KR 정적 TTF 폰트, Python의 `reportlab`·`pymupdf`가 필요하다.

```bash
python Tools/build_topic_pdfs.py --source-dir /path/to/sources --font-dir /path/to/fonts
python Tools/validate_knowledge.py --source-dir /path/to/sources
```

</details>
