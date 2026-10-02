# WBS-app

이차전지 설계·공정 자료를 탐색하고 프로젝트 작업 WBS와 연결하기 위한 문서·데이터 기반이다. 현재 분류안·주제별 PDF·Markdown·Li 상세 예시를 제공하며 웹앱과 Hermes 자동 연결은 후속 구현이다.

## 먼저 볼 문서

- [지금까지의 요구사항과 GPT·GitHub·Hermes 연동계획](Docs/앱_요구사항과_연동계획.md)
- [설계·공정 세부 지식 분류안](Docs/이차전지_지식분류안.md)
- [LFP·LMFP·NCM·LMO 분류와 구성 원소](Docs/양극재_분류와_구성원소.md)
- [Li: 기본 물성·이온·금속 음극 상세](Knowledge/materials/Li.md) · [PDF](References/topics/13_Li_리튬.pdf)
- [주제별 PDF와 원본 쪽수 대응표](Docs/원본_자료_배치표.md)
- [저장 구조·기록·검토 규칙](Docs/저장_구조와_기록규칙.md)
- [재사용 메모의 아이디어 분류](Knowledge/ideas/재사용_아이디어.md)
- [작업 현황과 후속 구현](Docs/작업_현황.md)

## 표준 지침

- [이차전지 WBS 국제·국내 표준 및 전극 지침](Docs/이차전지_WBS_표준_지침.md)

## 제작·검증

`Data/taxonomy.json`은 탐색 계층과 관계, `Data/topic-manifest.json`은 문서·원본 위치, `Data/source-page-map.json`은 PDF 쪽수 대응을 관리한다. 상세가 아직 없는 말단 항목은 앞으로 작성할 대상으로 구분한다.

PDF 재생성에는 원본 2개와 Noto Sans KR 정적 TTF 폰트, Python의 `reportlab`·`pymupdf`가 필요하다.

```bash
python Tools/build_topic_pdfs.py --source-dir /path/to/sources --font-dir /path/to/fonts
python Tools/validate_knowledge.py --source-dir /path/to/sources
```
