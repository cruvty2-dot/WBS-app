"""Regenerate the WBS README and per-item links without common-PDF fallback."""
import json
from pathlib import Path
from collections import defaultdict
from build_wbs_pdfs import filename
ROOT=Path(__file__).resolve().parents[1]

def main():
    tax=json.loads((ROOT/'Data/taxonomy.json').read_text())
    data=json.loads((ROOT/'Data/wbs-learning.json').read_text())
    manifest=json.loads((ROOT/'Data/wbs-pdf-manifest.json').read_text())
    items={x['id']:x for x in data['items']}; pdfs={x['id']:x for x in manifest['pdfs']}
    children=defaultdict(list)
    for n in tax['nodes']:children[n['parent_id']].append(n['id'])
    for n in tax['nodes']:
        if n['id']=='battery':continue
        x=items[n['id']];old=n.get('article_paths',[])
        if 'reference_article_paths' not in n:n['reference_article_paths']=old
        stem=filename(x['wbs'],x['label']);md=f'Knowledge/items/{stem}.md'
        n['article_paths']=[md] if (ROOT/md).is_file() else []
        n['wbs_code']=x['wbs'];n['pdf_path']=pdfs[n['id']]['pdf_path']
    (ROOT/'Data/taxonomy.json').write_text(json.dumps(tax,ensure_ascii=False,indent=2)+'\n')
    lines=['# Battery Study - 배터리 공부','',
      '이차전지의 소재·설계·평가·제조공정을 **설계 / 공정** 두 축으로 공부한다. 분류를 유지하며 각 항목의 내용을 대화로 하나씩 다듬는다.','',
      '## 목차','',
      '| 문서·목차 | 역할 |','| --- | --- |',
      '| [전체 WBS 목차](#전체-wbs-목차) | 195개 항목의 학습 상태·핵심·항목 PDF |',
      '| [1. 설계](#1-설계) | 소재, 전극, 셀, 평가·열화, 차세대전지 |',
      '| [2. 공정](#2-공정) | 원료, 전극, 조립, 화성, 품질, 재사용·재활용, 공급망 |',
      '| [문서 구성과 수정](#문서-구성과-수정) | 선수학습 양식과 상위·하위 PDF 갱신 규칙 |',
      '| [분류·기준·근거](#분류기준근거) | 분류 원칙·소재와 원소·핵심 설명의 참고자료 |',
      '| [아이디어·프로젝트·기록 양식](#아이디어프로젝트기록-양식) | 학습문서·분석 기록·작업 요청 양식 |',
      '| [운영·연동 계획](#운영연동-계획) | 저장·수정 규칙과 후속 앱 계획 |','',
      '## 전체 WBS 목차','',
      '**상위 PDF는 그 항목과 모든 하위 단계의 내용을 포함한다.** `2 공정`은 `2.1~2.7`과 그 아래 모든 세부 항목을, `2.1 원료·소재 제조`는 `2.1.1~2.1.5`를 포함한다. 가장 아래 항목 PDF는 해당 항목만 담는다. PDF 책갈피로 WBS 번호를 바로 찾을 수 있다.','',
      '번호는 분류 위치를 뜻한다. 선수학습 순서는 각 문서 앞부분, 이후 연계학습은 끝부분에 번호와 항목명으로 적는다.','',
      '**미학습은 학습 진도, 핵심 요약·상세문서는 자료의 준비 수준**이다. 학습 완료 기록이 없어서 현재 상태를 미학습으로 두었다. 상세내용이 없는 항목에도 짧은 핵심 요약을 마련했으며, 총괄적인 공통 PDF로 대신 연결하지 않는다.','',
      '현재 상세문서: **Li·NCM·LFP·LMFP·LMO 및 2.1.1~2.1.5**. 나머지는 핵심 요약이며, 상위 합본에서도 각 항목의 수준을 표시한다.','']
    headers=['| WBS 번호 | 분류·학습 항목 | 학습 상태 | 핵심 | 연결 문서 |','| --- | --- | --- | --- | --- |']
    def subtree(k):
        yield k
        for c in children[k]:yield from subtree(c)
    def row(k):
        x=items[k];p=pdfs[k];name='**'+x['label']+'**' if children[k] else x['label']
        mode='하위 전체 PDF' if children[k] else ('상세 PDF' if x['content_level']=='상세문서' else '요약 PDF')
        link=f"[{mode}]({p['pdf_path']})"
        md=f"Knowledge/items/{filename(x['wbs'],x['label'])}.md"
        if (ROOT/md).is_file():link=f'[내용]({md}) · '+link
        return f"| {x['wbs']} | {name} | {x['learning_status']} | {x['core']} | {link} |"
    for axis in children['battery']:
        lines += [f"## {items[axis]['wbs']}. {items[axis]['label']}",'',*headers,row(axis),'']
        for branch in children[axis]:
            lines += [f"### {items[branch]['wbs']} {items[branch]['label']}",'',*headers]
            lines += [row(k) for k in subtree(branch)]+['']
    lines += ['## 문서 구성과 수정','',
      '1. **선수학습**: 먼저 공부하면 좋은 WBS 번호와 항목명.','2. **먼저 알아둘 기초**: 이해에 필요한 정의·단위·기준 몇 가지.','3. **핵심 내용**: 해당 항목의 원리·특성·예시·확인할 증거.','4. **참고 근거**: 공식 자료·원 논문·계산의 가정.','5. **이후 연계학습**: 다음에 공부하면 좋은 WBS 번호와 항목명.','',
      '본문에 개편 내역을 넣는 대신 학습 내용을 쓴다. 관련 내용을 길게 설명할 필요가 있으면 해당 WBS 문서에서 다룬다. 상위 합본의 마지막에도 이후 연계학습을 둔다.','',
      '내용 원본은 [항목별 학습 데이터](Data/wbs-learning.json) 한 곳에서 관리한다. 이를 수정해 해당 항목 PDF와 모든 상위 합본, README·상세 Markdown을 함께 생성한다. 같은 파일 경로에 최신본을 반영하며 이전 버전은 Git 변경 이력에 남긴다.','',
      '[전체 항목별 PDF 목록](References/wbs/README.md) · [학습문서 양식](Templates/학습문서.md)','',
      '<details>','<summary>원본을 재배치한 이전 자료</summary>','',
      '[이전 주제별 자료 14종](References/topics/README.md)은 원문 표·그림을 확인하기 위한 참고자료다. 현재 WBS 항목의 PDF 연결에는 사용하지 않는다. 필요한 내용·그림은 항목을 상세화할 때 해당 항목에 맞게 검토해 반영한다.','',
      '</details>','',
      '## 분류·기준·근거','',
      '| 문서 | 역할 |','| --- | --- |',
      '| [이차전지 지식 분류안](Docs/이차전지_지식분류안.md) | 유지하는 설계·공정 분류 |',
      '| [양극재 분류와 구성 원소](Docs/양극재_분류와_구성원소.md) | 소재 계열·화합물·구성 원소의 관계 |',
      '| [핵심 설명의 참고자료](Docs/WBS_핵심설명_참고자료.md) | 공식 자료·원 논문과 항목별 근거 ID |',
      '| [표준 및 전극 지침](Docs/이차전지_WBS_표준_지침.md) | 기존 표준 관련 참고자료와 확인 범위 |',
      '| [원본 자료 배치표](Docs/원본_자료_배치표.md) | 이전 자료의 원문 쪽수 확인 |','',
      '## 아이디어·프로젝트·기록 양식','',
      '| 문서·양식 | 역할 |','| --- | --- |',
      '| [학습문서](Templates/학습문서.md) | 선수학습부터 이후 연계학습까지 |',
      '| [재사용 아이디어](Knowledge/ideas/재사용_아이디어.md) | 질문·검증 과제 |',
      '| [재사용 검증 WBS](Projects/재사용_검증_WBS_예시.md) | 실제 작업·산출물 예시 |',
      '| [작업 요청](Templates/작업요청.md) | 목표·입력·범위·완료 기준 |',
      '| [분석 기록](Templates/analysis-record.json) | 시료·조건·처리·해석·검토 상태 |','',
      '## 운영·연동 계획','',
      '| 문서 | 역할 |','| --- | --- |',
      '| [요구사항과 연동 계획](Docs/앱_요구사항과_연동계획.md) | 앱과 GPT·GitHub·Hermes 계획 |',
      '| [저장 구조와 기록 규칙](Docs/저장_구조와_기록규칙.md) | 자료 저장·변경 규칙 |',
      '| [작업 현황](Docs/작업_현황.md) | 완료 자료와 후속 구현 |','',
      '<details>','<summary>제작·검증 방법</summary>','',
      '```bash','python Tools/build_wbs_pdfs.py --font-dir /path/to/fonts','python Tools/build_wbs_index.py','python Tools/validate_wbs_pdfs.py','python Tools/validate_knowledge.py','```','',
      'Noto Sans KR 정적 TTF 400·700과 `reportlab`·`pymupdf`가 필요하다. [PDF 목록 데이터](Data/wbs-pdf-manifest.json)에 각 합본의 포함 항목과 쪽수 범위를 기록한다.','',
      '탐색 웹앱과 Hermes 실제 연결은 후속 구현이며, 현재 자료는 GitHub의 문서·PDF로 읽는다.','',
      '</details>','']
    (ROOT/'README.md').write_text('\n'.join(lines))
    p=['# WBS 항목별 PDF','',
       '상위 항목은 모든 하위 단계를 포함한다. 세부 항목은 해당 부분만 연다. 파일명과 PDF 제목은 WBS 번호·항목명을 따른다. 특수문자와 공백은 파일명에서 밑줄로 정리한다.','',
       '학습 상태는 미학습으로 시작하며, 요약 자료가 존재해도 학습 완료를 뜻하지 않는다.','',
       '| WBS 번호 | 항목 | 범위 | 본 항목 수준 | 쪽수 | PDF |','| --- | --- | --- | --- | --- | --- |']
    for x in manifest['pdfs']:
        mode=f"하위 전체 ({len(x['included_ids'])}개 항목)" if children[x['id']] else '해당 항목만'
        p += [f"| {x['wbs']} | {x['label']} | {mode} | {x['content_level']} | {x['pdf_pages']} | [PDF]({Path(x['pdf_path']).name}) |"]
    (ROOT/'References/wbs/README.md').write_text('\n'.join(p)+'\n')
    s=['# WBS 핵심 설명의 참고자료','',
       '> 확인일: 2026-10-02','',
       '핵심 설명은 학습을 시작하기 위한 짧은 정리다. 세부 조성·성능·시험 조건은 항목을 상세화할 때 원 자료와 함께 다룬다. 학습 경로·기록 항목·확인 질문은 학습을 돕기 위한 제안이다.','',
       '각 항목의 `source_ids`는 [학습 데이터](../Data/wbs-learning.json)의 근거를 가리킨다. 원소 자료는 원소의 성질, 장비 자료는 분석 원리, 원 논문은 해당 조성·조건의 관찰 범위에 활용한다. 특정 논문의 결과를 소재 전체의 보편적 수치로 확대하지 않는다.','',
       '| 근거 ID | 자료 |','| --- | --- |']
    for sid,src in data['sources'].items():s+=[f"| {sid} | [{src['title']}]({src['url']}) |"]
    s+=['','## 항목별 근거','', '| WBS 번호 | 항목 | 근거 ID |','| --- | --- | --- |']
    for x in data['items']:s+=[f"| {x['wbs']} | {x['label']} | {', '.join(x['source_ids'])} |"]
    (ROOT/'Docs/WBS_핵심설명_참고자료.md').write_text('\n'.join(s)+'\n')
    # Preserve the old path as a navigation entry, not a competing content source.
    li=items['element.li'];li_md=f"../items/{filename(li['wbs'],li['label'])}.md"
    (ROOT/'Knowledge/materials/Li.md').write_text(f"# {li['wbs']} {li['label']}\n\n최신 학습문서는 [{li['wbs']} {li['label']}]({li_md})에서 읽는다. 선수학습과 기초를 먼저, 이후 연계학습을 마지막에 배치했다.\n\n[항목 PDF](../../{pdfs['element.li']['pdf_path']})\n")
    print('Updated WBS index:',len(items),'items')

if __name__=='__main__':main()
