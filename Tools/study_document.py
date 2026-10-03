"""Render page-based learning articles while keeping JSON as the content source."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib.utils import ImageReader

def render_pages(item, items, sources, root, styles, html):
    styles = dict(styles)
    for name, size, leading in [('body',11.2,18.6),('small',9.0,14.2),('h2',14,21),('h3',11.6,18),('table',10.0,16)]:
        styles[name] = ParagraphStyle('study_'+name, parent=styles[name], fontSize=size, leading=leading, spaceAfter=8)
    def para(text, style='body'): return Paragraph(html(text).replace('\n','<br/>'), styles[style])
    def label(k): return items[k]['wbs']+' '+items[k]['label']
    story=[]
    for i, page in enumerate(item['study_pages']):
        if i: story.append(PageBreak())
        else:
            has_children=any(x['wbs'].startswith(item['wbs']+'.') for x in items.values())
            mode='하위 항목 전체 포함' if has_children else '이 항목만 포함'
            story += [para(label(item['id']),'title'), para('학습 상태: '+item['learning_status']+' | '+mode,'small')]
        title=para(page['title'],'h2'); title.study_title=page['title']; story.append(title)
        for b in page['blocks']:
            kind=b['type']
            if kind=='text': story.append(para(b['text']))
            elif kind=='heading': story.append(para(b['text'],'h3'))
            elif kind=='note':
                box=Table([[para(b['text'])]], colWidths=[507])
                box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#EEF5F5')),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#BCD7D8')),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
                story += [box,Spacer(1,9)]
            elif kind in ('prerequisites','next'):
                story.append(para('선수학습' if kind=='prerequisites' else '이후 연계학습','h3'))
                story += [para(label(k),'small') for k in item['prerequisite_ids' if kind=='prerequisites' else 'next_ids']]
            elif kind=='basics':
                story.append(para('기초지식 - 먼저 알아둘 기초','h3'))
                for title,text in item['basics']: story += [para(title,'h3'),para(text)]
            elif kind=='core': story += [para('핵심 내용','h3'),para(item['core'])]
            elif kind=='table':
                rows=[[para(v,'table') for v in row] for row in [b['headers']]+b['rows']]
                table=Table(rows,colWidths=b['widths'],repeatRows=1,hAlign='LEFT')
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E3F0F0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F8FA')]),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#C9D8DF')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
                story += [table,Spacer(1,10)]
            elif kind=='figure':
                path=str(root/b['path']); width,height=ImageReader(path).getSize()
                image=Image(path,width=507,height=507*height/width)
                story += [KeepTogether([image,Spacer(1,5),para(b['caption'],'small')]),Spacer(1,7)]
            elif kind=='questions':
                for j,q in enumerate(item['review_questions'],1):story += [para(f'{j}. '+q['question'],'h3'),Spacer(1,30)]
            elif kind=='answers':
                for j,q in enumerate(item['review_questions'],1):story += [para(f'{j}. '+q['answer']),Spacer(1,3)]
            elif kind=='references':
                from html import escape
                for sid in b.get('source_ids',item['source_ids']):
                    s=sources[sid];tag=item['source_labels'][sid]
                    story += [Paragraph(html('['+tag+'] '+s['title'])+'<br/><link color="#087F82" href="'+escape(s['url'],quote=True)+'">'+escape(s['url'])+'</link>',styles['small'])]
            else:raise ValueError('Unknown study block: '+kind)
    return story

def markdown_pages(item, items, sources, pdf_path, root):
    def label(k):return items[k]['wbs']+' '+items[k]['label']
    lines=['# '+label(item['id']),'', '> 학습 상태: '+item['learning_status']+' | 문서 수준: 상세문서','', '[항목 PDF](../../'+pdf_path+')','']
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
