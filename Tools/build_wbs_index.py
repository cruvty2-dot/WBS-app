"""Regenerate the WBS README and per-item links without common-PDF fallback."""
import json
from pathlib import Path
from collections import defaultdict
from wbs_publication import filename
ROOT=Path(__file__).resolve().parents[1]

def main():
    tax=json.loads((ROOT/'Data/taxonomy.json').read_text(encoding='utf-8'))
    data=json.loads((ROOT/'Data/wbs-learning.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'Data/wbs-pdf-manifest.json').read_text(encoding='utf-8'))
    items={x['id']:x for x in data['items']}; pdfs={x['id']:x for x in manifest['pdfs']}
    children=defaultdict(list)
    for n in tax['nodes']:children[n['parent_id']].append(n['id'])
    for n in tax['nodes']:
        if n['id']=='battery':continue
        x=items[n['id']];old=n.get('article_paths',[])
        if 'reference_article_paths' not in n:n['reference_article_paths']=old
        stem=filename(x['wbs'],x['label']);md=f'Knowledge/items/{stem}.md'
        n['article_paths']=[md] if (ROOT/md).is_file() else []
        n['wbs_code']=x['wbs'];n['pdf_path']=pdfs.get(n['id'],{}).get('pdf_path')
    (ROOT/'Data/taxonomy.json').write_text(json.dumps(tax,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Battery Study - 배터리 공부','',
      '이차전지의 소재·설계·평가·제조공정을 **설계 / 공정** 두 축으로 공부한다. 분류를 유지하며 각 항목의 내용을 대화로 하나씩 다듬는다.','',
      '## 목차','',
      '| 문서·목차 | 역할 |','| --- | --- |',
      '| [전체 WBS 목차](#전체-wbs-목차) | 195개 항목의 학습 상태·핵심·항목 PDF |',
      '| [1. 설계](#1-설계) | 소재, 전극, 셀, 평가·열화, 차세대전지 |',
      '| [2. 공정](#2-공정) | 원료, 전극, 조립, 화성, 품질, 재사용·재활용, 공급망 |',
      '| [문서 구성과 수정](#문서-구성과-수정) | 학습문서 양식과 요청 시 채팅용 PDF 제공 규칙 |',
      '| [분류·기준·근거](#분류기준근거) | 분류 원칙·소재와 원소·핵심 설명의 참고자료 |',
      '| [아이디어·프로젝트·기록 양식](#아이디어프로젝트기록-양식) | 학습문서·분석 기록·작업 요청 양식 |',
      '| [운영·연동 계획](#운영연동-계획) | 저장·수정 규칙과 후속 앱 계획 |','',
      '## 전체 WBS 목차','',
      '**PDF는 가장 아래의 개별 항목에만 연결한다.** 상위 분류·하위 전체 합본은 만들지 않는다. 먼저 Markdown에서 내용을 학습·수정한다. 새 PDF는 별도 요청 시 GitHub 최신 내용을 바탕으로 이 채팅에서 제공하며 저장소에 자동 게시하지 않는다.','',
      '번호는 분류 위치를 뜻한다. 선수학습 순서는 각 문서 앞부분, 이후 연계학습은 끝부분에 번호와 항목명으로 적는다.','',
      '**미학습은 학습 진도, 작성 예정은 자료 준비 상태**다. 자료가 있다는 이유로 학습 완료로 기록하지 않는다. 자동 작성한 기본 요약·상세문서와 PDF를 정리하고 직접 수정한 Li·Ni·Mn의 본문을 보존했다. 기존 Li·Ni·Mn PDF도 삭제했다.','',
      '분류 번호·항목명은 유지한다. 나머지 항목은 함께 학습하고 검토하면서 하나씩 작성한다. Li·Ni·Mn·EIS는 학습중이다. 1.4.1.3 EIS와 예시 분석 결과는 1.4.1.3의 연결 문서에서 찾는다.','']
    headers=['| WBS 번호 | 분류·학습 항목 | 학습 상태 | 핵심 | 연결 문서 |','| --- | --- | --- | --- | --- |']
    def subtree(k):
        yield k
        for c in children[k]:yield from subtree(c)
    def row(k):
        x=items[k];p=pdfs.get(k);name='**'+x['label']+'**' if children[k] else x['label']
        links=[]
        md=f"Knowledge/items/{filename(x['wbs'],x['label'])}.md"
        if (ROOT/md).is_file():links.append(f'[내용]({md})')
        if p and not children[k] and (ROOT/p['pdf_path']).is_file():links.append(f"[상세 PDF]({p['pdf_path']})")
        if k=='method.eis':
            links=['[내용](Projects/eis-example-analysis/1.4.1.3%20EIS.md)', '[분석예시](Projects/eis-example-analysis/1.4.1.3%20EIS분석예시.md)']+links
        link=' · '.join(links) if links else ('—' if children[k] else '작성 예정')
        return f"| {x['wbs']} | {name} | {x['learning_status']} | {x['core'] or '작성 예정'} | {link} |"
    for axis in children['battery']:
        lines += [f"## {items[axis]['wbs']}. {items[axis]['label']}",'',*headers,row(axis),'']
        for branch in children[axis]:
            lines += [f"### {items[branch]['wbs']} {items[branch]['label']}",'',*headers]
            lines += [row(k) for k in subtree(branch)]+['']
    lines += ['## 문서 구성과 수정','',
      '1. **선수학습**: 모르면 본문의 핵심 설명을 따라가기 어려운 기존 항목. WBS 번호·이름만 적는다.','2. **기초지식**: 여기서 짧게 설명할 용어·기호·단위·존재 형태·가정.','3. **핵심내용**: 역할·기본 이론 → 작동 원리와 예제 → 특성을 좌우하는 조건 → 열화와 분석·해석 → 확인 문제와 해설.','4. **참고근거**: 주장·그림·계산의 출처와 적용 범위.','5. **연계학습**: 이해한 뒤 이어갈 항목의 WBS 번호·이름.','',
      '[학습문서 구성과 소분류 기준](Docs/학습문서_구성기준.md)에 선수학습 선정, 열화와 분석의 연결, 별도 항목을 만드는 기준을 정리한다. 실제 문서에는 해당 항목에 필요한 절을 골라 쓴다.','',
      '**수정 절차: Markdown에서 학습·확인·수정 → 목차 갱신 → GitHub 반영.** PDF는 별도 요청 시 GitHub 최신 내용을 바탕으로 가장 아래 항목만 제작해 이 채팅에서 제공하며 GitHub에 자동 업로드하지 않는다. 상위 합본은 만들지 않는다.','',
      '본문에 개편 내역을 넣는 대신 학습 내용을 쓴다. 관련 내용을 길게 설명할 필요가 있으면 해당 WBS 문서에서 다룬다.','',
      '항목 내용 원본은 [학습 데이터](Data/wbs-learning.json)에서 관리한다. 작성 예정인 내용과 삭제한 자료를 자동 생성하지 않는다. PDF 제작 범위는 [게시 정책](Data/publication-policy.json)에 기록하고 이전 버전은 Git 변경 이력에 남긴다.','',
      '[PDF 제공 안내](References/wbs/README.md) · [학습문서 양식](Templates/학습문서.md)','',
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
      '목차만 갱신: `python Tools/build_wbs_index.py`. PDF는 별도 요청을 받았을 때 `python Tools/build_wbs_pdfs.py --font-dir /path/to/fonts --only 요청한_하위_항목_ID --output-dir 저장소_밖_채팅_산출물_경로`로 생성한다. 상위 항목과 일괄 기본 생성은 지원하지 않는다.','',
      'Noto Sans KR 정적 TTF 400·700과 `reportlab`·`pymupdf`가 필요하다. [PDF 목록 데이터](Data/wbs-pdf-manifest.json)에 저장소의 PDF 목록은 비어 있다. 새 채팅용 PDF 제작 시 이 목록을 자동 갱신하지 않는다.','',
      '탐색 웹앱과 Hermes 실제 연결은 후속 구현이며, 현재 자료는 GitHub의 문서·PDF로 읽는다.','',
      '</details>','']
    (ROOT/'README.md').write_text('\n'.join(lines),encoding='utf-8')
    p=['# WBS 항목별 PDF','',
       '현재 저장소에 보관하는 WBS 학습 PDF는 없다. Li·Ni·Mn의 기존 PDF도 삭제했다. 새 PDF는 별도 요청 시 가장 아래의 개별 항목만 만들어 채팅에서 제공하고 저장소에 추가하지 않는다.','',
       'Li·Ni·Mn·EIS는 사용자가 읽고 수정하기 시작해 학습중이다. 최신 학습 상태와 내용은 Markdown과 학습 데이터를 기준으로 확인한다.','',
       '| WBS 번호 | 항목 | 범위 | 본 항목 수준 | 쪽수 | PDF |','| --- | --- | --- | --- | --- | --- |']
    for x in manifest['pdfs']:
        assert not children[x['id']], 'Parent PDF publication is disabled'
        mode='해당 항목만'
        p += [f"| {x['wbs']} | {x['label']} | {mode} | {x['content_level']} | {x['pdf_pages']} | [PDF]({Path(x['pdf_path']).name}) |"]
    (ROOT/'References/wbs/README.md').write_text('\n'.join(p)+'\n',encoding='utf-8')
    s=['# WBS 핵심 설명의 참고자료','',
       '> 확인일: '+data['updated_at'],'',
       '핵심 설명은 학습을 시작하기 위한 짧은 정리다. 세부 조성·성능·시험 조건은 항목을 상세화할 때 원 자료와 함께 다룬다. 학습 경로·기록 항목·확인 질문은 학습을 돕기 위한 제안이다.','',
       '각 항목의 `source_ids`는 [학습 데이터](../Data/wbs-learning.json)의 근거를 가리킨다. 원소 자료는 원소의 성질, 장비 자료는 분석 원리, 원 논문은 해당 조성·조건의 관찰 범위에 활용한다. 특정 논문의 결과를 소재 전체의 보편적 수치로 확대하지 않는다.','',
       '| 근거 ID | 자료 |','| --- | --- |']
    for sid,src in data['sources'].items():s+=[f"| {sid} | [{src['title']}]({src['url']}) |"]
    s+=['','## 항목별 근거','', '| WBS 번호 | 항목 | 근거 ID |','| --- | --- | --- |']
    for x in data['items']:s+=[f"| {x['wbs']} | {x['label']} | {', '.join(x['source_ids'])} |"]
    (ROOT/'Docs/WBS_핵심설명_참고자료.md').write_text('\n'.join(s)+'\n',encoding='utf-8')
    # Preserve the old path as a navigation entry, not a competing content source.
    li=items['element.li'];li_md=f"../items/{filename(li['wbs'],li['label'])}.md"
    li_pdf=('\n[항목 PDF](../../'+pdfs['element.li']['pdf_path']+')\n') if 'element.li' in pdfs else ''
    (ROOT/'Knowledge/materials/Li.md').write_text(f"# {li['wbs']} {li['label']}\n\n최신 학습문서는 [{li['wbs']} {li['label']}]({li_md})에서 읽는다. 선수학습과 기초를 먼저, 이후 연계학습을 마지막에 배치했다.\n{li_pdf}",encoding='utf-8')
    print('Updated WBS index:',len(items),'items')

if __name__=='__main__':main()
