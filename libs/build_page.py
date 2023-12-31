import os
import datetime
import base64
import pycmarkgfm
import io
from PIL import Image

from .toc_build import create_toc, create_keywords

TEMPLATES = {
    "head": "head.html",
    "title": "title_page.html",
    "page": "page.html",
    "pageHead": "page_header.html",
    "topic": "topic_title.html",
    "step": "step_explain.html"
}

SIZE_UNIT = 180   # 1を180pxとする


class PageManage:
    def __init__(self):
        self.page_num = 0
        self.new_page_flag = True

    def new_page(self):
        if not self.new_page_flag:
            return ""
        self.new_page_flag = False
        return get_element("pageHead", {"PAGENUM": f"{self.page_num}"})

    def set_new_page(self):
        self.new_page_flag = True
        self.page_num += 1

    def get(self):
        return self.page_num


def get_element(name: str, replace_map={}) -> str:
    path = os.path.join("./libs/templates/html", TEMPLATES[name])
    with open(path) as f:
        html = f.read()
    for t, txt in replace_map.items():
        if txt is None:
            continue
        html = html.replace(f"###{t}###", txt)
    return html


def create_page(content: str) -> str:
    return get_element("page", replace_map={"PAGECONTENT": content})


def create_content(base_path: str, child_path: str, conf: dict, keyname="") -> str:
    """ページやstepのコンフィグの、textまたはfileを読み取って、文字列を返す"""
    if conf.get("text") is not None:
        return "<br>\n".join(conf.get("text"))

    if conf.get("file") is None:
        print(f"XXX {child_path}/config.ymlの[{keyname}]にtextもfileも設定されていません")

    file_path = os.path.join(base_path, child_path, conf["file"])
    if not os.path.exists(file_path):
        print(f"XXX {child_path}/config.ymlの[{keyname}]にtextもfileも設定されていません")

    if file_path.endswith(".md"):
        with open(os.path.join(base_path, child_path, conf["file"])) as f:
            txt = f.read()
        return pycmarkgfm.markdown_to_html(txt)
        #return md.convert(txt)
    else:
        with open(os.path.join(base_path, child_path, conf["file"])) as f:
            return f.read()


def _get_image_info(img_path: str):
    img_type = os.path.splitext(img_path)[1].replace(".", "")
    img = Image.open(img_path)
    width, height = img.size
    with io.BytesIO() as buffer:
        img.save(buffer, format=img_type)  # ここでJPEG形式を指定していますが、必要に応じて変更できます
        binary_data = buffer.getvalue()
    return width, height, img_type, binary_data


def _get_image_size(width: int, height: int, size: str) -> str:
    x, y = list(map(lambda z: int(z)*SIZE_UNIT, size.split("x")))
    if width > height:
        return f"width:{x}px;height:auto;"
    else:
        return f"width:auto;height:{y}px;"


def get_image(base_path: str, page_path: str, path: str, img_size: str) -> str:
    """ファイルが指定された場合は、その画像ファイルを読み込んでBase64文字列を返す"""
    img_path = os.path.join(base_path, page_path, path)
    if path is None or not os.path.exists(img_path):
        return ""
    w, h, img_type, dat = _get_image_info(img_path)
    enc_dat = base64.b64encode(dat).decode()
    return f'<img style="{_get_image_size(w, h, img_size)}" src="data:image/{img_type};base64,{enc_dat}"/>'


def get_markdown_css(file_name: str):
    if file_name.endswith(".md"):
        return "markdown-body"
    return ""


def build(base_path: str, conf: dict) -> str:
    """config情報を元にマニュアルのHTMLを生成する"""
    #import pprint; pprint.pprint(conf)
    html = get_element("head")

    # タイトルページ作成
    date_str = datetime.datetime.now().strftime('%Y年%m月%d日')
    rep_map = {"TITLE": conf["title"], "ISSUER": conf.get("issuer", "株式会社ゼタント"), "ISSUEDATE": date_str}
    html += create_page(get_element("title", rep_map))

    topic_page_nums = dict()  # トピックとページ番号の対応表
    keyword_page_nums = dict() # キーワードとページ番号の対応表

    # セクション(ページ)作成
    sections_html = ""
    pm = PageManage()
    for topic in conf["topics"]:  #type: dict
        pm.set_new_page()
        topic_html = pm.new_page()  # ページヘッダにページ番号を書く
        topic_page_nums[topic.get("topic")] = pm.get()  # 目次のためにページ番号を覚えておく

        # トピックのタイトルヘッダを作る
        topic_description = create_content(base_path, topic["path"], topic.get("description"), "トピック定義")
        topic_txt_file = topic.get("description", {}).get("file", "")
        rep_map = {
            "TITLE": topic.get("topic"),
            "DESCRIPTION": topic_description,
            "MARKDOWN": get_markdown_css(topic_txt_file),
            "STEPMARGIN": str(conf.get("stepMargin", 48)),
        }
        topic_html += get_element("topic", rep_map)

        # ステップのコンテンツを並べる
        for num, step in enumerate(topic["steps"]):
            topic_html += pm.new_page()  # 改ページなら、ページヘッダにページ番号を書く

            # キャプション、テキスト、画像を入れる
            caption = step.get("caption", f"ステップ {num+1}")
            if caption == "":
                caption = f"ステップ {num+1}"

            text = create_content(base_path, topic["path"], step, f"ステップ定義:{caption}")
            rep_map = {"IMAGE": get_image(base_path, topic["path"], step.get("image"), step.get("imgSize")),
                       "CAPTION": caption,
                       "TEXT": text,
                       "MARKDOWN": get_markdown_css(step.get("file", "")),
                       "STEPMARGIN": str(conf.get("stepMargin", 48)),
                       }
            topic_html += get_element("step", rep_map)

            # 索引のためにページ番号を覚えておく
            for kw in step.get("keywords", []):
                if kw in keyword_page_nums:
                    keyword_page_nums[kw].add(pm.get())
                else:
                    keyword_page_nums[kw] = set([pm.get()])

            # 改ページが指示されていればダミーセクションを入れる
            if step.get("newPage", False):
                topic_html += '<section style="page-break-after: always"></section>\n'
                pm.set_new_page()
        sections_html += create_page(topic_html)

    # 目次作成
    html += create_toc(topic_page_nums)

    # 索引作成
    sections_html += create_keywords(keyword_page_nums)

    html = html + sections_html + "  </div>\n</body>\n</html>\n"
    return html

