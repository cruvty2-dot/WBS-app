# Battery Study 저장소 구조 안내

이 저장소는 이차전지 지식을 **설계 / 공정** 두 축으로 분류하고, 항목별 학습내용과 참고자료를 연결한다. 이 문서는 전체 파일 구조와 수정 경로를 안내한다. 개별 학습 항목은 [전체 학습 목차](README.md)에서 찾는다.

## 빠른 탐색

| 목적 | 시작할 문서 |
| --- | --- |
| 현재 목표·진행 상태·다음 작업 확인 | [학습 및 작업 계획](study-plan.md) |
| 에이전트의 자동 갱신·인계 규칙 확인 | [저장소 작업 지침](AGENTS.md) |
| 공부할 항목과 PDF 찾기 | [README](README.md) |
| 설계·공정 분류 전체 이해 | [이차전지 지식 분류안](Docs/이차전지_지식분류안.md) |
| 파일 역할과 수정 규칙 확인 | [저장 구조와 기록 규칙](Docs/저장_구조와_기록규칙.md) |
| 완료 범위와 남은 작업 확인 | [작업 현황](Docs/작업_현황.md) |
| 학습문서 작성 방식 확인 | [학습문서 양식](Templates/학습문서.md) |
| 앱과 외부 도구 연결 계획 확인 | [앱 요구사항과 연동 계획](Docs/앱_요구사항과_연동계획.md) |

## 폴더 구조

```text
battery-study/
├─ index.md                   저장소 전체 구조 안내
├─ study-plan.md              목표·진행 상태·다음 작업과 인계 정보
├─ AGENTS.md                  작업마다 계획·문서 링크를 갱신하는 지침
├─ README.md                  195개 학습 항목의 목차·상태·요약·링크
├─ Docs/                      분류·근거·운영·계획 문서
├─ Knowledge/
│  ├─ items/                  현재 WBS 항목별 상세 학습문서
│  ├─ topics/                 이전 주제별 자료의 보완 설명
│  ├─ materials/              기존 소재 문서 경로에서 최신 문서로 안내
│  └─ ideas/                  질문·아이디어와 검증 방향
├─ Data/                      분류·학습내용·자료 대응 관계의 JSON
├─ References/
│  ├─ wbs/                    항목별 PDF와 상위 합본 PDF
│  └─ topics/                 이전 원문 자료를 재배치한 주제별 PDF
├─ Projects/                  실제 작업·산출물 중심의 프로젝트 WBS 예시
├─ Templates/                 학습문서·작업요청·분석 기록 양식
├─ Tools/                     문서·PDF 생성 및 검증 스크립트
└─ LICENSE                    저장소 라이선스
```

Markdown 수량과 전체 파일 링크는 아래 자동 문서 목록에서 확인한다. `Knowledge/items`의 상세문서는 10개이며, 나머지 185개 학습 항목은 핵심 요약 수준이다.

## 학습 분류와 문서 내부 구조

| 1. 설계 | 2. 공정 |
| --- | --- |
| 1.1 소재·재료 | 2.1 원료·소재 제조 |
| 1.2 전극 설계 | 2.2 전극 제조 |
| 1.3 셀·시스템 설계 | 2.3 셀 조립 |
| 1.4 평가·분석·열화 | 2.4 화성·숙성·선별 |
| 1.5 다화학계·차세대전지 | 2.5 품질·공정 데이터 |
| | 2.6 재사용·재활용 |
| | 2.7 공급망·산업·직무 |

학습 항목의 WBS 번호는 분류 위치를 나타낸다. 학습 순서는 선수학습·이후 연계학습으로 따로 표현한다. 고유 분류 ID는 데이터에서 항목과 관련 링크를 연결하는 기준이다. 프로젝트 WBS는 작업·산출물·완료 기준을 나누는 별도 구조다.

항목별 상세 학습문서는 다음 순서를 따른다.

1. 제목: WBS 번호와 항목명
2. 학습 상태와 문서 수준
3. 선수학습
4. 먼저 알아둘 기초
5. 핵심 내용
6. 스스로 확인할 질문
7. 참고 근거
8. 이후 연계학습

**학습 상태와 자료 준비 수준은 별개다.** 상세문서가 있어도 학습 완료 기록이 없으면 미학습으로 표시한다.

## Markdown 문서 목록

### 분류·운영·근거: Docs

| 문서 | 역할 |
| --- | --- |
| [이차전지 지식 분류안](Docs/이차전지_지식분류안.md) | 분류 원칙과 전체 계층·고유 ID |
| [양극재 분류와 구성 원소](Docs/양극재_분류와_구성원소.md) | 소재 계열·화합물·원소의 관계 |
| [WBS 핵심 설명 참고자료](Docs/WBS_핵심설명_참고자료.md) | 근거 자료와 항목별 근거 ID |
| [이차전지 WBS 표준 지침](Docs/이차전지_WBS_표준_지침.md) | 지식 분류·작업 WBS 구분 및 표준 참조 범위 |
| [원본 자료 배치표](Docs/원본_자료_배치표.md) | 주제별 자료와 원본 페이지의 대응 |
| [저장 구조와 기록 규칙](Docs/저장_구조와_기록규칙.md) | 파일 역할·기록 필드·작성·개정 규칙 |
| [앱 요구사항과 연동 계획](Docs/앱_요구사항과_연동계획.md) | 화면·저장·외부 도구 연결 계획 |
| [작업 현황](Docs/작업_현황.md) | 완료된 자료·보완 과제·후속 구현 |

### 현재 상세 학습문서: Knowledge/items

| WBS 번호 | 문서 |
| --- | --- |
| 1.1.1.1.1 | [Li: 원소·Li⁺·금속 음극](Knowledge/items/1.1.1.1.1_Li_원소·Li⁺·금속_음극.md) |
| 1.1.2.1.1.1 | [NCM](Knowledge/items/1.1.2.1.1.1_NCM.md) |
| 1.1.2.1.2.1 | [LFP](Knowledge/items/1.1.2.1.2.1_LFP.md) |
| 1.1.2.1.2.2 | [LMFP](Knowledge/items/1.1.2.1.2.2_LMFP.md) |
| 1.1.2.1.3.1 | [LMO](Knowledge/items/1.1.2.1.3.1_LMO.md) |
| 2.1.1 | [입고·보관·수입검사](Knowledge/items/2.1.1_입고·보관·수입검사.md) |
| 2.1.2 | [전구체·공침·결정화](Knowledge/items/2.1.2_전구체·공침·결정화.md) |
| 2.1.3 | [리튬화·소성](Knowledge/items/2.1.3_리튬화·소성.md) |
| 2.1.4 | [분쇄·분급·도핑·코팅](Knowledge/items/2.1.4_분쇄·분급·도핑·코팅.md) |
| 2.1.5 | [흑연·Si계 소재 제조](Knowledge/items/2.1.5_흑연·Si계_소재_제조.md) |

### 이전 주제별 자료의 보완 설명: Knowledge/topics

이 문서들은 이전 주제별 PDF와 원본 쪽수를 연결한다. 현재 항목별 상세문서와 구분해서 읽는다.

| 번호 | 문서 |
| --- | --- |
| 00 | [학습지도·용어·공식](Knowledge/topics/00_guide.md) |
| 01 | [소재 특성·결정·전자구조](Knowledge/topics/01_material-basics.md) |
| 02 | [전기화학 기초](Knowledge/topics/02_electrochemistry.md) |
| 03 | [양극재·반응·열화](Knowledge/topics/03_cathodes.md) |
| 04 | [음극재·리튬 석출](Knowledge/topics/04_anodes.md) |
| 05 | [전해질·바인더·보조소재](Knowledge/topics/05_electrolyte-and-additives.md) |
| 06 | [전극·셀 설계 계산](Knowledge/topics/06_electrode-and-cell-design.md) |
| 07 | [셀 조립·함침·화성](Knowledge/topics/07_assembly-and-formation.md) |
| 08 | [평가·기기분석·데이터 해석](Knowledge/topics/08_evaluation-and-analysis.md) |
| 09 | [열화·안전·차세대전지](Knowledge/topics/09_degradation-and-next-generation.md) |
| 10 | [전극 제조·혼합·도공·건조·압연](Knowledge/topics/10_electrode-manufacturing.md) |
| 11 | [건식전극·스케일업·품질](Knowledge/topics/11_dry-electrode-and-quality.md) |
| 12 | [공급망·재사용·재활용·직무](Knowledge/topics/12_recycling-and-applications.md) |

### 안내·아이디어·프로젝트·양식·자료 목록

| 문서 | 역할 |
| --- | --- |
| [기존 Li 문서 경로](Knowledge/materials/Li.md) | 최신 항목 문서와 PDF로 안내 |
| [재사용 아이디어](Knowledge/ideas/재사용_아이디어.md) | 아이디어를 질문·검증 과제로 정리 |
| [재사용 검증 프로젝트 WBS 예시](Projects/재사용_검증_WBS_예시.md) | 작업·산출물·완료 기준의 구조 예시 |
| [학습문서 양식](Templates/학습문서.md) | 항목별 학습문서 공통 구성 |
| [작업요청 양식](Templates/작업요청.md) | 목적·입력·조건·산출물·완료 기준 |
| [WBS PDF 목록](References/wbs/README.md) | 항목별 PDF와 상위 합본 탐색 |
| [이전 주제별 PDF 목록](References/topics/README.md) | 원문 표·그림 확인용 자료 탐색 |

## 데이터와 생성 결과의 관계

| 데이터 | 역할 |
| --- | --- |
| [taxonomy.json](Data/taxonomy.json) | 분류 ID·부모·관련 항목·문서 경로 |
| [wbs-learning.json](Data/wbs-learning.json) | 학습 상태·요약·선수학습·상세내용·근거의 내용 원본 |
| [wbs-pdf-manifest.json](Data/wbs-pdf-manifest.json) | PDF별 포함 항목·쪽수·경로 |
| [topic-manifest.json](Data/topic-manifest.json) | 이전 주제별 자료·원본·문서의 관계 |
| [source-page-map.json](Data/source-page-map.json) | 재배치 PDF와 원본 페이지 대응 |
| [분석 기록 양식](Templates/analysis-record.json) | 향후 분석 결과의 구조화 기록 양식 |

```text
Data/taxonomy.json + Data/wbs-learning.json
    │
    ├─ Tools/build_wbs_pdfs.py
    │    ├─ Knowledge/items/*.md
    │    ├─ References/wbs/*.pdf
    │    └─ Data/wbs-pdf-manifest.json
    │
    └─ Tools/build_wbs_index.py (PDF 목록 생성 후 실행)
         ├─ README.md
         ├─ References/wbs/README.md
         ├─ Docs/WBS_핵심설명_참고자료.md
         ├─ Knowledge/materials/Li.md
         └─ Data/taxonomy.json의 문서·PDF 연결 갱신
```

상위 PDF는 해당 항목과 모든 하위 항목을 재귀적으로 포함한다. 가장 아래 항목 PDF는 해당 항목만 포함한다.

## 수정·검증 방법

항목별 학습내용을 수정할 때는 `Data/wbs-learning.json`을 먼저 바꾸고 상세 Markdown·PDF·목차를 다시 생성한다. 생성된 Markdown만 수정하면 다음 생성 때 변경이 덮어써질 수 있다. 이 `index.md`는 수동으로 관리하는 구조 안내다.

| 도구 | 용도 |
| --- | --- |
| [sync_document_index.py](Tools/sync_document_index.py) | 수동 구조 안내를 유지하며 전체 Markdown 링크 목록 동기화·파일 링크 검증 |
| [build_wbs_pdfs.py](Tools/build_wbs_pdfs.py) | 항목별·상위 합본 PDF와 상세 Markdown 생성 |
| [build_wbs_index.py](Tools/build_wbs_index.py) | README·PDF 목록·근거 목록과 문서 연결 갱신 |
| [build_topic_pdfs.py](Tools/build_topic_pdfs.py) | 이전 원문 자료의 주제별 PDF 제작 |
| [validate_wbs_pdfs.py](Tools/validate_wbs_pdfs.py) | WBS PDF 구조·포함 범위 검증 |
| [validate_knowledge.py](Tools/validate_knowledge.py) | 분류 관계·로컬 문서 링크·자료 대응 검증 |

저장소 루트에서 다음 순서로 실행한다. PDF 생성에는 `reportlab`, `pymupdf`, Noto Sans KR 정적 TTF 400·700이 필요하다.

```bash
python Tools/build_wbs_pdfs.py --font-dir /path/to/fonts
python Tools/build_wbs_index.py
python Tools/validate_wbs_pdfs.py
python Tools/validate_knowledge.py
```

현재 저장소의 중심은 문서와 PDF다. 탐색 웹앱·기록 편집·외부 실행자·Hermes의 실제 연결은 [작업 현황](Docs/작업_현황.md)에 기재된 후속 구현 범위다.

<!-- document-index:start -->
## 자동 문서 목록

Markdown 총 42개. 이 목록은 `Tools/sync_document_index.py`로 갱신한다.

### 루트

- [저장소 작업 지침](AGENTS.md)
### Docs

- [WBS 핵심 설명의 참고자료](Docs/WBS_핵심설명_참고자료.md)
- [이차전지 지식·WBS 앱 요구사항과 연동 계획](Docs/앱_요구사항과_연동계획.md)
- [양극재 분류와 구성 원소의 연결](Docs/양극재_분류와_구성원소.md)
- [원본 자료 배치표](Docs/원본_자료_배치표.md)
- [이차전지 WBS 앱: 국제·국내 표준 참조 지침](Docs/이차전지_WBS_표준_지침.md)
- [이차전지 지식 분류안](Docs/이차전지_지식분류안.md)
- [작업 현황](Docs/작업_현황.md)
- [저장 구조와 기록 규칙](Docs/저장_구조와_기록규칙.md)
### Knowledge/ideas

- [배터리 재사용·재생 아이디어](Knowledge/ideas/재사용_아이디어.md)
### Knowledge/items

- [1.1.1.1.1 Li: 원소·Li⁺·금속 음극](Knowledge/items/1.1.1.1.1_Li_원소·Li⁺·금속_음극.md)
- [1.1.2.1.1.1 NCM](Knowledge/items/1.1.2.1.1.1_NCM.md)
- [1.1.2.1.2.1 LFP](Knowledge/items/1.1.2.1.2.1_LFP.md)
- [1.1.2.1.2.2 LMFP](Knowledge/items/1.1.2.1.2.2_LMFP.md)
- [1.1.2.1.3.1 LMO](Knowledge/items/1.1.2.1.3.1_LMO.md)
- [2.1.1 입고·보관·수입검사](Knowledge/items/2.1.1_입고·보관·수입검사.md)
- [2.1.2 전구체·공침·결정화](Knowledge/items/2.1.2_전구체·공침·결정화.md)
- [2.1.3 리튬화·소성](Knowledge/items/2.1.3_리튬화·소성.md)
- [2.1.4 분쇄·분급·도핑·코팅](Knowledge/items/2.1.4_분쇄·분급·도핑·코팅.md)
- [2.1.5 흑연·Si계 소재 제조](Knowledge/items/2.1.5_흑연·Si계_소재_제조.md)
### Knowledge/materials

- [1.1.1.1.1 Li: 원소·Li⁺·금속 음극](Knowledge/materials/Li.md)
### Knowledge/topics

- [학습지도·용어·공식](Knowledge/topics/00_guide.md)
- [소재 특성·결정·전자구조](Knowledge/topics/01_material-basics.md)
- [전기화학 기초](Knowledge/topics/02_electrochemistry.md)
- [양극재·반응·열화](Knowledge/topics/03_cathodes.md)
- [음극재·리튬 석출](Knowledge/topics/04_anodes.md)
- [전해질·바인더·보조소재](Knowledge/topics/05_electrolyte-and-additives.md)
- [전극·셀 설계 계산](Knowledge/topics/06_electrode-and-cell-design.md)
- [셀 조립·함침·화성](Knowledge/topics/07_assembly-and-formation.md)
- [평가·기기분석·데이터 해석](Knowledge/topics/08_evaluation-and-analysis.md)
- [열화·안전·차세대전지](Knowledge/topics/09_degradation-and-next-generation.md)
- [전극 제조·혼합·도공·건조·압연](Knowledge/topics/10_electrode-manufacturing.md)
- [건식전극·스케일업·품질](Knowledge/topics/11_dry-electrode-and-quality.md)
- [공급망·재사용·재활용·직무](Knowledge/topics/12_recycling-and-applications.md)
### Projects

- [재사용 진단 검증 프로젝트 WBS 예시](Projects/재사용_검증_WBS_예시.md)
### 루트

- [Battery Study - 배터리 공부](README.md)
### References/topics

- [주제별 PDF](References/topics/README.md)
### References/wbs

- [WBS 항목별 PDF](References/wbs/README.md)
### Templates

- [작업 요청](Templates/작업요청.md)
- [WBS 번호 항목 이름](Templates/학습문서.md)
### 루트

- [Battery Study 저장소 구조 안내](index.md)
- [학습 및 작업 계획](study-plan.md)

<!-- document-index:end -->
