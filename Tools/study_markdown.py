"""Render written learning content as Markdown without creating PDFs."""
from pathlib import Path

def markdown_pages(item, items, sources, pdf_path, root):
    def label(k):return items[k]['wbs']+' '+items[k]['label']
    lines=['# '+label(item['id']),'', '> 학습 상태: '+item['learning_status']+' | 문서 수준: 상세문서','', *(['[기존 보존 PDF](../../'+pdf_path+')',''] if pdf_path else [])]
    for page in item['study_pages']:
        lines += ['## '+page['title'],'']
        for b in page['blocks']:
            kind=b['type']
            if kind=='text':lines += [b['text'],'']
            elif kind=='heading':lines += ['### '+b['text'],'']
            elif kind=='note':lines += ['> '+b['text'],'']
            elif kind in ('prerequisites','next'):
                lines += ['### '+('선수학습' if kind=='prerequisites' else '이후 연계학습'),'']+['- '+label(k) for k in item['prerequisite_ids' if kind=='prerequisites' else 'next_ids']]+['']
            elif kind=='basics':
                lines += ['### 기초지식 - 먼저 알아둘 기초','']
                for title,text in item['basics']:lines += ['#### '+title,'',text,'']
            elif kind=='core':lines += ['### 핵심 내용','',item['core'],'']
            elif kind=='table':
                def cells(row):return ' | '.join(v.replace('|','\\|').replace('\n','<br>') for v in row)
                lines += ['| '+cells(b['headers'])+' |','| '+' | '.join(['---']*len(b['headers']))+' |']
                lines += ['| '+cells(row)+' |' for row in b['rows']]+['']
            elif kind=='figure':lines += ['!['+b['caption']+']('+Path(b['path']).name+')','',b['caption'],'']
            elif kind in ('questions','answers'):
                for j,q in enumerate(item['review_questions'],1):lines += [f'{j}. '+q['question' if kind=='questions' else 'answer'],'']
            elif kind=='references':
                for sid in b.get('source_ids',item['source_ids']):
                    s=sources[sid];lines += ['- ['+item['source_labels'][sid]+'] ['+s['title']+']('+s['url']+')']
                lines += ['']
    return '\n'.join(lines)
