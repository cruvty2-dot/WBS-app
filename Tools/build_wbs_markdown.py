"""Refresh written learning articles without generating or publishing PDFs."""
import argparse
import json
from pathlib import Path
from study_markdown import markdown_pages
from wbs_publication import filename

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', nargs='+', help='Written item IDs to refresh')
    args = parser.parse_args()
    data = json.loads((ROOT / 'Data/wbs-learning.json').read_text(encoding='utf-8'))
    items = {item['id']: item for item in data['items']}
    selected = set(args.only or [key for key, item in items.items() if item['content_level'] != '미작성'])
    if selected - items.keys():
        parser.error('Unknown item IDs: ' + ', '.join(sorted(selected - items.keys())))
    if any(items[key]['content_level'] == '미작성' for key in selected):
        parser.error('Unwritten items must be developed before generating Markdown')
    manifest = json.loads((ROOT / 'Data/wbs-pdf-manifest.json').read_text(encoding='utf-8'))
    pdfs = {entry['id']: entry['pdf_path'] for entry in manifest['pdfs']}
    output = ROOT / 'Knowledge/items'
    output.mkdir(parents=True, exist_ok=True)
    for key in selected:
        item = items[key]
        if not item.get('study_pages'):
            parser.error('Written items require study_pages: ' + key)
        text = markdown_pages(item, items, data['sources'], pdfs.get(key), ROOT)
        (output / (filename(item['wbs'], item['label']) + '.md')).write_text(text, encoding='utf-8')
    print('Updated written Markdown articles:', len(selected))


if __name__ == '__main__':
    main()
