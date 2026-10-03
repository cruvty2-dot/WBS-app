"""Dependency-free helpers for on-request publication of individual WBS leaves."""
import re


def filename(wbs, label):
    label = re.sub(r'[\\/:*?"<>|\s]+', '_', label).strip('_')
    return f'{wbs}_{label}'


def selected_leaf_ids(requested, items, children):
    if not requested:
        raise ValueError('Specify the individually requested item IDs with --only.')
    selected = set(requested)
    unknown = selected - set(items)
    if unknown:
        raise ValueError('Unknown item IDs: ' + ', '.join(sorted(unknown)))
    parents = sorted(k for k in selected if children.get(k))
    if parents:
        raise ValueError('Parent/compiled PDFs are disabled: ' + ', '.join(parents))
    unwritten = sorted(k for k in selected if items[k]['content_level'] == '미작성')
    if unwritten:
        raise ValueError('Write and review the content before requesting a PDF: ' + ', '.join(unwritten))
    return selected
