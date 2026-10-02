"""Build topic PDFs, preserving source page graphics and provenance.

Usage: python Tools/build_topic_pdfs.py --source-dir ../upload --font-dir ../tmp/fonts
Dependencies: reportlab, pymupdf
Fonts: NotoSansKR-400.ttf and NotoSansKR-700.ttf (supply separately).
"""
import argparse, hashlib, json, re, tempfile
from pathlib import Path
from html import escape
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT=Path(__file__).resolve().parents[1]
NAVY=colors.HexColor('#123144'); TEAL=colors.HexColor('#007E87')
GRAY=colors.HexColor('#52636E'); LIGHT=colors.HexColor('#ECF3F5')
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def safe(text):
    return escape(text).replace('⁺','+').replace('⁻','-').replace('¹','1').replace('²','2').replace('³','3').replace('ₓ','x').replace('₄','4').replace('₆','6')

def register(font_dir):
    pdfmetrics.registerFont(TTFont('KR',str(font_dir/'NotoSansKR-400.ttf')))
    pdfmetrics.registerFont(TTFont('KRB',str(font_dir/'NotoSansKR-700.ttf')))
    pdfmetrics.registerFontFamily('KR',normal='KR',bold='KRB',italic='KR',boldItalic='KRB')

ST={}
def styles():
    ST.update({
      'body':ParagraphStyle('body',fontName='KR',fontSize=10.5,leading=16.5,textColor=NAVY,spaceAfter=9,wordWrap='CJK'),
      'small':ParagraphStyle('small',fontName='KR',fontSize=8.5,leading=13,textColor=GRAY,spaceAfter=6,wordWrap='CJK'),
      'h1':ParagraphStyle('h1',fontName='KRB',fontSize=20,leading=28,textColor=NAVY,spaceAfter=16,wordWrap='CJK'),
      'h2':ParagraphStyle('h2',fontName='KRB',fontSize=13,leading=20,textColor=TEAL,spaceBefore=10,spaceAfter=7,wordWrap='CJK'),
      'h3':ParagraphStyle('h3',fontName='KRB',fontSize=11,leading=17,textColor=TEAL,spaceBefore=8,spaceAfter=6,wordWrap='CJK'),
      'table':ParagraphStyle('table',fontName='KR',fontSize=8.5,leading=12.5,textColor=NAVY,wordWrap='CJK'),
    })
def p(text,style='body'): return Paragraph(safe(text),ST[style])
def header_footer(c,doc):
    c.setFillColor(TEAL);c.rect(44,800,507,3,fill=1,stroke=0)
    c.setFont('KR',8);c.setFillColor(GRAY)
    c.drawString(44,812,'이차전지 지식 · WBS 학습자료')
    c.drawString(44,27,'주제별 개편 | 2026-10-02')
    c.drawRightString(551,27,str(doc.page))
def build(path,story):
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=58,bottomMargin=48,title=path.stem,author='Battery WBS project')
    doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)
def table(rows,widths):
    data=[[p(x,'table') for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#B9CCD2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return t
def range_text(ranges):return ', '.join(str(a) if a==b else f'{a}-{b}' for a,b in ranges)
def md_inline(text):
    text=text.replace('**','').replace('`','')
    return re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',text)
def li_story(path):
    lines=path.read_text(encoding='utf-8').splitlines(); out=[]; i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[md_inline(x.strip()) for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[: -]+',x) for x in cells): rows.append(cells)
                i+=1
            out.append(table(rows,[135,195,177] if len(rows[0])==3 else [507/len(rows[0])]*len(rows[0])));out.append(Spacer(1,10));continue
        if line.startswith('# '): out.append(p(line[2:],'h1'))
        elif line.startswith('## '): out.append(p(line[3:],'h2'))
        elif line.startswith('>'): out.append(p(md_inline(line[1:].strip()),'small'))
        elif line.startswith('- '): out.append(p('• '+md_inline(line[2:]),'small' if 'https://' in line else 'body'))
        else: out.append(p(md_inline(line)))
        i+=1
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,required=True);ap.add_argument('--font-dir',type=Path,required=True);args=ap.parse_args()
    register(args.font_dir);styles()
    manifest=read('Data/topic-manifest.json'); taxonomy=read('Data/taxonomy.json'); byid={n['id']:n for n in taxonomy['nodes']}
    source_meta={s['id']:s for s in manifest['sources']}; sources={}
    for s in manifest['sources']:
        path=args.source_dir/s['filename']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=s['sha256']:raise ValueError('Source version changed: '+s['filename'])
        if path.suffix=='.pdf': sources[s['id']]=fitz.open(path)
    mapping=[]; summary=[]
    with tempfile.TemporaryDirectory() as temp:
        for topic in manifest['topics']:
            final=ROOT/topic['pdf_path'];final.parent.mkdir(parents=True,exist_ok=True)
            intro=Path(temp)/(topic['number']+'.pdf')
            story=[p('TOPIC '+topic['number'],'small'),p(topic['title'],'h1'),p(topic['summary']),p('분류와 자료 위치','h2')]
            story.append(p(' / '.join(byid[id]['label'] for id in topic['category_ids']),'small'))
            rows=[['원본 자료','추출한 원본 쪽수']]
            for s in topic['sources']:rows.append([source_meta[s['source_id']]['filename'],range_text(s['ranges'])])
            story+=[table(rows,[315,192]),Spacer(1,12),p('이번 개편에서 보완한 내용','h2')]
            for section in topic['sections'][:2]:story+=[p(section['title'],'h3'),p(section['text'])]
            story+=[PageBreak(),p('해석 기준과 적용','h1')]
            for section in topic['sections'][2:]:story+=[p(section['title'],'h2'),p(section['text'])]
            story+=[p('확인할 질문·실습','h2'),p(topic['exercise']),p('원문을 읽는 방법','h2'),p('다음 페이지부터 원문의 그래프·표·질문을 보존한 참고 페이지다. 인쇄 쪽수·절 번호는 원본 기준이다. PDF 책갈피와 별도 쪽수 대응표를 이용한다. 이 보완 설명은 원문 전체의 독립적인 사실검증이나 규격 적합성 검토를 뜻하지 않는다.','small')]
            if topic['external_refs']:
                story+=[p('보완 설명의 근거','h2')]
                for ref in topic['external_refs']:story.append(p(ref,'small'))
            build(intro,story);doc=fitz.open(intro);intro_count=len(doc)
            toc=[[1,'주제 안내와 보완 설명',1],[2,'해석 기준과 적용',2]]
            for src in topic['sources']:
                source_id=src['source_id'];original=sources[source_id];src_start=len(doc)+1;localmap={}
                toc.append([1,source_meta[source_id]['filename']+' 원문',src_start])
                for a,b in src['ranges']:
                    for old_page in range(a,b+1):
                        doc.insert_pdf(original,from_page=old_page-1,to_page=old_page-1,links=False)
                        new_page=len(doc);localmap[old_page]=new_page
                        mapping.append({'topic_id':topic['id'],'pdf_path':topic['pdf_path'],'pdf_page':new_page,'source_id':source_id,'source_filename':source_meta[source_id]['filename'],'source_page':old_page})
                added=set()
                for _,label,old_page in original.get_toc():
                    if old_page in localmap and (old_page,label) not in added:
                        toc.append([2,label,localmap[old_page]]);added.add((old_page,label))
            doc.set_toc(toc);doc.set_metadata({'title':topic['title'],'author':'Battery WBS project','subject':'주제별 재구성·보완 설명·원본 페이지 연결','keywords':'battery,WBS,design,process'})
            doc.save(final,garbage=4,deflate=True);doc.close()
            topic['intro_pages']=intro_count;topic['total_pdf_pages']=intro_count+sum(b-a+1 for src in topic['sources'] for a,b in src['ranges'])
            summary.append((topic,final))
        final=ROOT/'References/topics/13_Li_리튬.pdf'
        build(final,li_story(ROOT/'Knowledge/materials/Li.md'))
        d=fitz.open(final);toc=[]
        for i,page in enumerate(d):
            txt=page.get_text()
            for n in range(1,7):
                headings={1:'기본 물성',2:'배터리에서의 역할',3:'금속 음극의 용량·전위',4:'열화와 검증',5:'설계·공정에서 연결할 질문',6:'출처'}
                if f'{n}. {headings[n]}' in txt:toc.append([1,headings[n],i+1])
        d.set_toc(toc); d.saveIncr();d.close()
    for src in sources.values():src.close()
    (ROOT/'Data/topic-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'Data/source-page-map.json').write_text(json.dumps({'schema_version':'1.0','page_number_basis':'1-based PDF physical page','mappings':mapping,'omitted_pages':manifest['omitted_pages'],'omission_reason':manifest['omission_reason']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text='# 原本'.replace('原本','원본')+' 자료 배치표\n\n> 2026-10-02 | PDF 실제 쪽수는 1부터 센다. 기존 페이지의 인쇄 숫자는 원본 쪽수다.\n\n'
    text+='원본의 본문·질문·그림을 보존하고 새 보완 설명을 앞에 추가했다. 기존 표지·통합 목차·부 표지는 새 주제 안내로 대체했다. 서로 다른 주제가 한 원본 쪽에 있으면 맥락을 보존하기 위해 페이지 전체를 유지했다.\n\n## 주제별 파일\n\n| 주제 | 원본 쪽수 | 개편 PDF | 보완 페이지 |\n| --- | --- | --- | --- |\n'
    for t,_ in summary:
        src=' / '.join(s['source_id']+' '+range_text(s['ranges']) for s in t['sources'])
        text+=f"| {t['title']} | {src} | [{Path(t['pdf_path']).name}](../{t['pdf_path']}) · {t['total_pdf_pages']}쪽 | 앞 {t['intro_pages']}쪽 |\n"
    text+='| Li 상세 | 새로 작성; 관련 원본 13, 41-44, 50-51, 74, 95-96 | [13_Li_리튬.pdf](../References/topics/13_Li_리튬.pdf) | 문서 전체 |\n'
    text+='\n## 원본 자료 식별\n\n'
    for s in manifest['sources']:text+=f"- `{s['id']}`: {s['filename']} · SHA-256 `{s['sha256']}`\n"
    text+='\n## PDF 쪽수 대응\n\n| 개편 PDF | 개편 쪽수 | 원본 파일 | 원본 쪽수 |\n| --- | --- | --- | --- |\n'
    for m in mapping:text+=f"| {Path(m['pdf_path']).name} | {m['pdf_page']} | {m['source_filename']} | {m['source_page']} |\n"
    text+='\n## 생략한 안내 페이지\n\n'
    for src,pages in manifest['omitted_pages'].items():text+=f"- {source_meta[src]['filename']}: {', '.join(map(str,pages))}쪽. {manifest['omission_reason']}\n"
    text+='\n## 변경과 검토 범위\n\n공통 양극 반응식의 대상, Li 원소·이온·금속 구분, 로딩량·밀도·공극률·N/P의 기준, EIS 등 관찰과 원인 판단의 범위, 회수율의 분모를 보완했다. 원문의 개별 그래프와 모든 수치·문헌 전체를 독립 검증 완료했다는 의미는 아니다.\n'
    (ROOT/'Docs/원본_자료_배치표.md').write_text(text,encoding='utf-8')
    print(json.dumps({'topic_pdfs':len(summary),'li_pdf':str(final),'source_pages_preserved':len(mapping),'authored_intro_pages':sum(t['intro_pages'] for t,_ in summary)},ensure_ascii=False))

if __name__=='__main__':main()
