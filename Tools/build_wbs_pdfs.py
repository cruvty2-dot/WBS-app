"""Generate item PDFs and recursive parent compilations from one content source.

Edit Data/wbs-learning.json, then run:
python Tools/build_wbs_pdfs.py --font-dir /path/to/fonts
Requires reportlab, pymupdf, NotoSansKR-400.ttf and NotoSansKR-700.ttf.
Classification/order comes from Data/taxonomy.json; existing WBS codes must match.
"""
import argparse, io, json, re, tempfile
from collections import defaultdict
from html import escape
from pathlib import Path
import fitz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from study_document import render_pages, markdown_pages

ROOT=Path(__file__).resolve().parents[1]
NAVY=colors.HexColor('#203949'); TEAL=colors.HexColor('#087F82')
GRAY=colors.HexColor('#536675'); LIGHT=colors.HexColor('#EEF5F5')

SUB='₀₁₂₃₄₅₆₇₈₉₋ₓᵧₐᵦ'; SUB_ASC='0123456789-xyab'
SUP='⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹'; SUP_ASC='+-0123456789'
def plain_symbols(s):
    return s.translate(str.maketrans(SUB+SUP,SUB_ASC+SUP_ASC)).replace('→','->').replace('⇄','<->').replace('≈','~').replace('≤','<=').replace('≥','>=')
def pdf_html(s):
    s=escape(s.replace('≤','<=').replace('≥','>=')).replace('→','-&gt;').replace('⇄','&lt;-&gt;').replace('≈','~')
    s=re.sub('['+SUB+']+(?:\\.['+SUB+']+)*(?:[xyz])?',lambda m:'<sub>'+m[0].translate(str.maketrans(SUB,SUB_ASC))+'</sub>',s)
    s=re.sub('['+SUP+']+',lambda m:'<super>'+m[0].translate(str.maketrans(SUP,SUP_ASC))+'</super>',s)
    for symbol in 'μΩ∫':
        s=s.replace(symbol,'<font name="Math">'+symbol+'</font>')
    return s

def filename(wbs,label):
    label=re.sub(r'[\\/:*?"<>|\s]+','_',label).strip('_')
    return f'{wbs}_{label}'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--font-dir',type=Path,required=True)
    ap.add_argument('--only',nargs='+',help='Changed item IDs; rebuild these items and their ancestors only')
    args=ap.parse_args()
    data=json.loads((ROOT/'Data/wbs-learning.json').read_text())
    taxonomy=json.loads((ROOT/'Data/taxonomy.json').read_text())
    items={x['id']:x for x in data['items']}; children=defaultdict(list)
    for n in taxonomy['nodes']: children[n['parent_id']].append(n['id'])
    expected={}
    def assign(parent,prefix=''):
        for i,k in enumerate(children[parent],1):
            expected[k]=f'{prefix}.{i}' if prefix else str(i);assign(k,expected[k])
    assign('battery')
    cached={}
    selected=set(expected)
    if args.only:
        unknown=set(args.only)-set(expected)
        if unknown:ap.error('Unknown item IDs: '+', '.join(sorted(unknown)))
        cached={x['id']:x for x in json.loads((ROOT/'Data/wbs-pdf-manifest.json').read_text())['pdfs']}
        parents={n['id']:n['parent_id'] for n in taxonomy['nodes']}
        selected=set()
        for k in args.only:
            while k!='battery': selected.add(k); k=parents[k]
    assert set(items)==set(expected)
    for k,x in items.items():
        assert x['wbs']==expected[k],('number changed',k)
        assert x['label']==next(n['label'] for n in taxonomy['nodes'] if n['id']==k)
        for rel in x['prerequisite_ids']+x['next_ids']: assert rel in items and rel!=k
        for sid in x['source_ids']: assert sid in data['sources']
    for name,weight in [('KR','400'),('KRB','700')]:
        pdfmetrics.registerFont(TTFont(name,str(args.font_dir/f'NotoSansKR-{weight}.ttf')))
    math_font = args.font_dir/'DejaVuSans.ttf'
    if not math_font.exists():
        math_font = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    if not math_font.exists():
        import matplotlib
        math_font = Path(matplotlib.get_data_path())/'fonts/ttf/DejaVuSans.ttf'
    pdfmetrics.registerFont(TTFont('Math',str(math_font)))
    pdfmetrics.registerFontFamily('KR',normal='KR',bold='KRB',italic='KR',boldItalic='KRB')
    st={
        'title':ParagraphStyle('title',fontName='KRB',fontSize=20,leading=28,textColor=NAVY,spaceAfter=12,wordWrap='CJK'),
        'h2':ParagraphStyle('h2',fontName='KRB',fontSize=12,leading=18,textColor=TEAL,spaceBefore=12,spaceAfter=6,keepWithNext=True,wordWrap='CJK'),
        'h3':ParagraphStyle('h3',fontName='KRB',fontSize=10.5,leading=16,textColor=NAVY,spaceBefore=6,spaceAfter=4,keepWithNext=True,wordWrap='CJK'),
        'body':ParagraphStyle('body',fontName='KR',fontSize=10.2,leading=16.2,textColor=NAVY,spaceAfter=7,wordWrap='CJK'),
        'small':ParagraphStyle('small',fontName='KR',fontSize=8.6,leading=13,textColor=GRAY,spaceAfter=6,wordWrap='CJK'),
        'table':ParagraphStyle('table',fontName='KR',fontSize=9.5,leading=14,textColor=NAVY,wordWrap='CJK')}
    def p(s,style='body'):return Paragraph(pdf_html(s),st[style])
    def label(k):return items[k]['wbs']+' '+items[k]['label']
    def relations(ids):return [p(label(k),'small') for k in ids] or [p('별도 지정 없음','small')]
    def refs(sids):
        out=[]
        for sid in dict.fromkeys(sids):
            src=data['sources'][sid];url=escape(src['url'],quote=True)
            out+=[Paragraph(escape(src['title'])+f'<br/><link href="{url}" color="#087F82">'+escape(src['url'])+'</link>',st['small'])]
        return out
    def footer(c,doc,x):
        c.setFillColor(TEAL);c.rect(44,800,507,2.5,fill=1,stroke=0)
        c.setFont('KR',8);c.setFillColor(GRAY)
        c.drawString(44,813,'Battery Study | WBS 학습자료')
        c.drawString(44,26,x['wbs']+' | '+x.get('updated_at',data['updated_at']))
    def write(path,story,x):
        doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=57,bottomMargin=48,title=label(x['id']),author='Battery Study')
        def bookmark(flowable):
            if hasattr(flowable,'study_title'):
                key='study_'+str(doc.page)
                doc.canv.bookmarkPage(key)
                doc.canv.addOutlineEntry(flowable.study_title,key,level=0)
        doc.afterFlowable=bookmark
        doc.build(story,onFirstPage=lambda c,d:footer(c,d,x),onLaterPages=lambda c,d:footer(c,d,x))
    def next_story(x):return [p('이후 연계학습','h2'),*relations(x['next_ids'])]
    def story(x):
        if x.get('study_pages'):return render_pages(x,items,data['sources'],ROOT,st,pdf_html)
        k=x['id'];has_children=bool(children[k]);out=[p(label(k),'title')]
        mode='하위 항목 전체 포함' if has_children else '이 항목만 포함'
        out+=[p(f"학습 상태: {x['learning_status']} | 본 항목: {x['content_level']} | {mode}",'small'),p('선수학습','h2'),*relations(x['prerequisite_ids']),p('먼저 알아둘 기초','h2')]
        basics=x['basics']
        if not basics:
            basics=[(items[r]['label'],items[r]['core']) for r in x['prerequisite_ids'][:2]]
        if not basics:basics=[('학습 관점',x['core'])]
        for title,text in basics:out+=[p(title,'h3'),p(text)]
        out += [p('핵심 내용','h2')]
        if x['sections']:
            for title,text in x['sections']:out+=[p(title,'h3'),p(text)]
            out+=[p('스스로 확인할 질문','h2'),p(x['question'])]
        else:
            out+=[p(x['core']),p('현재는 학습을 시작하기 위한 핵심 요약이다. 구체적인 예시·수식·측정 조건은 이 항목을 공부하면서 상세화한다.','small')]
        if has_children:
            out+=[p('포함되는 하위 항목','h2')]
            rows=[[p('WBS 번호','table'),p('항목','table')]]+[[p(items[r]['wbs'],'table'),p(items[r]['label'],'table')] for r in children[k]]
            table=Table(rows,colWidths=[115,392],repeatRows=1)
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#CEDCDE')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            out+=[table,Spacer(1,8),p('각 하위 항목의 하위 단계까지 모두 포함한다. PDF 책갈피에서 원하는 WBS 번호로 이동할 수 있다.','small')]
        sids=x['source_ids']+[sid for r in x['prerequisite_ids'][:2] for sid in items[r]['source_ids']]
        out+=[p('참고 근거','h2'),*refs(sids)]
        if not has_children:out+=next_story(x)
        return out
    pdfdir=ROOT/'References/wbs';pdfdir.mkdir(parents=True,exist_ok=True)
    md_dir=ROOT/'Knowledge/items';md_dir.mkdir(parents=True,exist_ok=True)
    summaries=[]
    def subtree(k):
        yield k
        for c in children[k]:yield from subtree(c)
    def build(k,temp):
        if k not in selected:return cached[k]
        x=items[k];stem=filename(x['wbs'],x['label']);own=temp/(stem+'.pdf')
        write(own,story(x),x);doc=fitz.open(own);own_pages=len(doc);toc=[[1,label(k),1]]
        toc.extend([[2,title,page] for _,title,page in doc.get_toc()])
        ranges=[{'id':k,'start_page':1,'end_page':len(doc),'own_content_only':True}]
        for c in children[k]:
            child_info=build(c,temp);path=ROOT/child_info['pdf_path'];offset=len(doc)
            with fitz.open(path) as child:
                doc.insert_pdf(child)
                toc.extend([[level+1,title,page+offset] for level,title,page in child.get_toc()])
            ranges.extend([{**r,'start_page':r['start_page']+offset,'end_page':r['end_page']+offset} for r in child_info['content_ranges']])
        if children[k]:
            end=temp/(stem+'_end.pdf')
            write(end,[p(label(k)+' - 학습의 연결','title'),*next_story(x)],x)
            toc.append([2,label(k)+' 이후 연계학습',len(doc)+1])
            with fitz.open(end) as ending:doc.insert_pdf(ending)
        doc.set_toc(toc)
        # Page numbers are local to the opened PDF, even when it is a compilation.
        for i,page in enumerate(doc):
            page.draw_rect(fitz.Rect(430,805,551,827),color=None,fill=(1,1,1),overlay=True)
            page.insert_text((490,816),f'{i+1} / {len(doc)}',fontsize=8,color=(.32,.4,.46),overlay=True)
        doc.set_metadata({'title':label(k),'author':'Battery Study','subject':('하위 항목 전체 포함' if children[k] else '단일 WBS 항목'),'keywords':x['wbs']+',battery,WBS'})
        final=pdfdir/(stem+'.pdf')
        staged=temp/(stem+'_final.pdf');doc.save(staged,garbage=4,deflate=True)
        staged.replace(final)
        info={'id':k,'wbs':x['wbs'],'label':x['label'],'pdf_path':str(final.relative_to(ROOT)),'pdf_pages':len(doc),'own_pages':own_pages,'included_ids':list(subtree(k)),'content_ranges':ranges,'content_level':x['content_level'],'learning_status':x['learning_status']}
        doc.close();summaries.append(info);return info
    with tempfile.TemporaryDirectory(prefix='wbs-pdf-') as t:
        for k in children['battery']:build(k,Path(t))
    lookup={**cached,**{x['id']:x for x in summaries}};ordered=[lookup[x['id']] for x in data['items']]
    (ROOT/'Data/wbs-pdf-manifest.json').write_text(json.dumps({'schema_version':'1.0','updated_at':data['updated_at'],'rule':'each PDF includes its node and all descendants; one canonical content source','pdfs':ordered},ensure_ascii=False,indent=2)+'\n')
    # Readable versions of the developed articles; JSON remains the canonical source.
    for x in data['items']:
        if x['content_level']!='상세문서':continue
        if x.get('study_pages'):
            stem=filename(x['wbs'],x['label'])
            (md_dir/(stem+'.md')).write_text(markdown_pages(x,items,data['sources'],lookup[x['id']]['pdf_path'],ROOT))
            continue
        stem=filename(x['wbs'],x['label']);lines=['# '+label(x['id']),'',f"> 학습 상태: {x['learning_status']} | 문서 수준: 상세문서",'',f"[항목 PDF](../../{lookup[x['id']]['pdf_path']})",'','## 선수학습','']
        lines += ['- '+label(k) for k in x['prerequisite_ids']]
        lines += ['','## 먼저 알아둘 기초','']
        for title,text in x['basics']:lines+=['### '+title,'',text,'']
        lines+=['## 핵심 내용','']
        for title,text in x['sections']:lines+=['### '+title,'',text,'']
        lines+=['## 스스로 확인할 질문','',x['question'],'','## 참고 근거','']
        for sid in x['source_ids']:
            s=data['sources'][sid];lines+=['- ['+s['title']+']('+s['url']+')']
        lines+=['','## 이후 연계학습','']+['- '+label(k) for k in x['next_ids']]+['']
        (md_dir/(stem+'.md')).write_text('\n'.join(lines))
    print(json.dumps({'pdf_files':len(ordered),'developed_articles':sum(x['content_level']=='상세문서' for x in data['items']),'design_pages':lookup['design']['pdf_pages'],'process_pages':lookup['process']['pdf_pages'],'pdf_bytes':sum((ROOT/x['pdf_path']).stat().st_size for x in ordered)},ensure_ascii=False))

if __name__=='__main__':main()
