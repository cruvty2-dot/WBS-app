"""Check taxonomy integrity, local links and source PDF page fidelity."""
import argparse, hashlib, json, re
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-dir',type=Path);args=parser.parse_args()
    taxonomy=read('Data/taxonomy.json');nodes=taxonomy['nodes'];ids={n['id'] for n in nodes};assert len(ids)==len(nodes),'duplicate IDs'
    byid={n['id']:n for n in nodes}
    assert [n['id'] for n in nodes if n['parent_id'] is None]==['battery']
    assert {n['id'] for n in nodes if n['parent_id']=='battery'}=={'design','process'}
    for n in nodes:
        assert n['parent_id'] is None or n['parent_id'] in ids
        for rel in n.get('related_node_ids',[])+n.get('contains_element_ids',[]):assert rel in ids,(n['id'],rel)
        for path in n['article_paths']:assert (ROOT/path).is_file(),path
        seen=set();current=n['id']
        while current is not None:
            assert current not in seen,'cycle';seen.add(current);current=byid[current]['parent_id']
    for md in ROOT.rglob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
            if not target.startswith(('http:','https:','mailto:','#')):assert (md.parent/target.split('#')[0]).exists(),(md,target)
    manifest=read('Data/topic-manifest.json');maps=read('Data/source-page-map.json')['mappings'];seen={};pdf_cache={};source_cache={}
    for t in manifest['topics']:
        for key in ['markdown_path','pdf_path']:assert (ROOT/t[key]).is_file()
        d=fitz.open(ROOT/t['pdf_path']);assert len(d)==t['total_pdf_pages'];d.close()
        for id in t['category_ids']:assert id in ids
    for m in maps:
        key=(m['source_id'],m['source_page']);assert key not in seen,'duplicate preserved source page';seen[key]=m
        pdf=pdf_cache.setdefault(m['pdf_path'],fitz.open(ROOT/m['pdf_path']))
        assert 1<=m['pdf_page']<=len(pdf)
        if args.source_dir:
            src=source_cache.setdefault(m['source_id'],fitz.open(args.source_dir/m['source_filename']))
            original=src[m['source_page']-1].get_pixmap(matrix=fitz.Matrix(.75,.75),alpha=False)
            derived=pdf[m['pdf_page']-1].get_pixmap(matrix=fitz.Matrix(.75,.75),alpha=False)
            assert (original.width,original.height,original.samples)==(derived.width,derived.height,derived.samples),('render changed',m)
    if args.source_dir:
        for s in manifest['sources']:
            path=args.source_dir/s['filename'];assert hashlib.sha256(path.read_bytes()).hexdigest()==s['sha256']
            if s['id'] in manifest['omitted_pages']:
                doc=fitz.open(path);included={p for src,p in seen if src==s['id']};omitted=set(manifest['omitted_pages'][s['id']]);assert included.isdisjoint(omitted);assert included|omitted==set(range(1,len(doc)+1));doc.close()
    for d in list(pdf_cache.values())+list(source_cache.values()):d.close()
    print(json.dumps({'taxonomy_nodes':len(nodes),'preserved_pages':len(maps),'local_links':'ok','source_render_fidelity':'all mapped pages identical' if args.source_dir else 'not checked'},ensure_ascii=False))
if __name__=='__main__':main()
