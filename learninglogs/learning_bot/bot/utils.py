import re

from lxml.html.clean import Cleaner


def html_to_telegram(html):
    allow_tags = [
        'b', 'strong', 'i', 'u',
        'em', 'ins', 's', 'strike',
        'del', 'a', 'code', 'pre',
    ]

    youtube_re = r'<iframe .*src="|".*></iframe>'
    header_re = re.compile(r'<head[^a-z][\s\S]*</head>')

    tg_html = re.sub(r'<(/?)h[1-6](?=\s|>)', r'<\1strong', html)
    tg_html = re.sub(youtube_re, r'', tg_html)
    tg_html = header_re.sub('', tg_html)

    cleaner = Cleaner(
        scripts=True,
        embedded=True,
        meta=True,
        page_structure=True,
        links=True,
        style=True,
        allow_tags=allow_tags
    )
    return cleaner.clean_html(tg_html)[5:-6]
