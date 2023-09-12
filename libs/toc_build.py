"""
目次および索引を作成する
"""


def create_toc(page_map: dict):
    html = '<section class="p-4" style="page-break-after: always">\n'
    html += '<div class="text-2xl mb-4">目次</div>'
    for topic, num in page_map.items():
        html += '<div class="grid-cols-2 grid">\n'
        html += f'<div class="col-span-1">{topic}</div>\n'
        html += f'<div class="col-span-1">{num}</div>\n'
        html += f'</div>\n'
    return html + "</section>\n"


def create_keywords(page_map: dict):
    html = '<section class="p-4" style="page-break-after: always">\n'
    html += '<div class="text-2xl mb-4">索引</div>'
    for kw, nums in page_map.items():
        n = map(lambda x: str(x), sorted(nums))
        html += '<div class="grid-cols-2 grid">\n'
        html += f'<div class="col-span-1">{kw}</div>\n'
        html += f'<div class="col-span-1">{", ".join(n)}</div>\n'
        html += f'</div>\n'
    return html + "</section>\n"
