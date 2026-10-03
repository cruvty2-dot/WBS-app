"""Check WBS scope, ordering, filenames, learning content and individual leaf PDFs."""
import argparse, json, re
from collections import defaultdict
from pathlib import Path
import fitz
from build_wbs_pdfs import filename, plain_symbols
ROOT=Path(__file__).resolve().parents[1]
def compact(s):return re.sub(r'\s+','',plain_symbols(s))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--render-check',action='store_true');args=ap.parse_args()
    tax=json.loads((ROOT/'Data/taxonomy.json').read_text(encoding='utf-8'))
    data=json.loads((ROOT/'Data/wbs-learning.json').read_text(encoding='utf-8'));items={x['id']:x for x in data['items']}
    man=json.loads((ROOT/'Data/wbs-pdf-manifest.json').read_text(encoding='utf-8'));pdfs={x['id']:x for x in man['pdfs']}
    children=defaultdict(list)
    for n in tax['nodes']:children[n['parent_id']].append(n['id'])
    def subtree(k):
        yield k
        for c in children[k]:yield from subtree(c)
    assert len(items)==195 and set(pdfs)<=set(items)
    assert len({x['wbs'] for x in items.values()})==195
    assert len(list((ROOT/'References/wbs').glob('*.pdf')))==len(pdfs)
    visiting=set();done=set()
    def prerequisites(k):
        assert k not in visiting,(k,'prerequisite cycle')
        if k in done:return
        visiting.add(k)
        for rel in items[k]['prerequisite_ids']:
            assert rel in items and rel!=k
            prerequisites(rel)
        visiting.remove(k);done.add(k)
    for k in items:prerequisites(k)
    pages=0;merged=0;shape_checked=0
    for k,m in pdfs.items():
        x=items[k];assert not children[k], (k,'parent PDF disabled')
        assert m['included_ids']==[k]
        assert Path(m['pdf_path']).stem==filename(x['wbs'],x['label'])
        with fitz.open(ROOT/m['pdf_path']) as doc:
            assert len(doc)==m['pdf_pages'];pages+=len(doc)
            assert doc.metadata['title']==x['wbs']+' '+x['label']
            first=compact(doc[0].get_text());assert compact(x['wbs']+' '+x['label']) in first
            assert first.index('선수학습')<first.index('먼저알아둘기초')<first.index('핵심내용')
            assert '이후연계학습' in compact(doc[-1].get_text())
            toc=doc.get_toc();assert toc[0]==[1,x['wbs']+' '+x['label'],1]
            if x.get('study_pages'):
                assert m['own_pages']==len(x['study_pages']),(k,'unexpected page overflow')
                own_toc=[t[1] for t in toc[1:] if t[2]<=m['own_pages']]
                assert own_toc==[p['title'] for p in x['study_pages']]
                assert set(x['source_labels'])==set(x['source_ids'])
                assert len(set(x['source_labels'].values()))==len(x['source_ids'])
                listed=[]
                for study_page in x['study_pages']:
                    for block in study_page['blocks']:
                        if block['type']=='figure':assert (ROOT/block['path']).is_file()
                        if block['type']=='references':listed.extend(block.get('source_ids',x['source_ids']))
                        body=' '.join([block.get('text',''),block.get('caption','')]+[v for row in block.get('rows',[]) for v in row])
                        for citation in re.findall(r'\[(\d+(?:,\s*\d+)*)\]',body):
                            assert set(re.split(r',\s*',citation))<=set(x['source_labels'].values()),(k,citation,'undefined reference')
                assert listed==x['source_ids'],(k,'missing or duplicate source listing')
            for r in m['content_ranges']:
                text=compact(''.join(doc[p].get_text() for p in range(r['start_page']-1,r['end_page'])))
                ix=items[r['id']]
                assert compact(ix['wbs']+' '+ix['label']) in text,(k,r['id'],'missing title')
                # Developed bodies use sections; summary bodies use their core sentence.
                expected_text=ix['sections'][0][1] if ix['sections'] else ix['core']
                assert compact(expected_text) in text,(k,r['id'],'missing body')
            assert m['own_pages']==len(doc)
            for page in doc:
                for image in page.get_images(full=True):
                    width,height=image[2:4]
                    for rect in page.get_image_rects(image[0]):
                        assert 38<=rect.x0 and rect.x1<=558 and 45<=rect.y0 and rect.y1<=794,(k,'image outside body',rect)
                        assert abs(rect.width/rect.height-width/height)<.001,(k,'distorted image',rect)
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            assert '\ufffd' not in span['text'] and '\x00' not in span['text']
                            a,b,c,d=span['bbox'];assert a>=38 and c<=558 and b>=10 and d<=830,(k,span)
                shape_checked+=1
    md=(ROOT/'README.md').read_text(encoding='utf-8')
    rows=[line for line in md.splitlines() if re.match(r'^\| [12](?:\.\d+)* \|',line)]
    assert len(rows)==195
    assert sum('References/wbs/' in r for r in rows)==len(pdfs)
    assert all('References/topics/' not in r for r in rows)
    assert '이번 개편에서 보완한 내용' not in md
    print(json.dumps({'pdfs':len(pdfs),'total_pdf_pages':pages,'all_wbs_scopes':'ok','all_names':'ok','all_content':'ok','all_text_bounds':'ok','readme_rows':len(rows)},ensure_ascii=False))
if __name__=='__main__':main()
