import os
import datetime
import base64

from .toc_build import create_toc, create_keywords


TEMPLATES = {
    "head": "head.html",
    "title": "title_page.html",
    "page": "page.html",
    "pageHead": "page_header.html",
    "topic": "topic_title.html",
    "step": "step_explain.html"
}


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
    elif conf.get("file") is not None:
        with open(os.path.join(base_path, child_path, conf["file"])) as f:
            return f.read()
    print(f"XXX {child_path}/config.ymlの[{keyname}]にtextもfileも設定されていません")


def get_image(base_path: str, page_path: str, path: str, img_size: str) -> str:
    """ファイルが指定された場合は、その画像ファイルを読み込んでBase64文字列を返す"""
    img_path = os.path.join(base_path, page_path, path)
    if path is None or not os.path.exists(img_path):
        return ""
    with open(img_path, "rb") as f:
        dat = f.read()
    enc_dat = base64.b64encode(dat).decode()
    return f'<img style="{get_image_size(img_size)}" src="data:image/png;base64,{enc_dat}"/>'


def get_image_size(size: str) -> str:
    if size == "2x2":
        return "width:360px;height:360px"
    elif size == "2x1":
        return "width:360px;height:180px"
    elif size == "1x2":
        return "width:180px;height:360px"
    else:
        return "width:180px;height:180px"


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

    # TODO: セクション(ページ)作成
    sections_html = ""
    pm = PageManage()
    for topic in conf["topics"]:  #type: dict
        pm.set_new_page()
        topic_html = pm.new_page()  # ページヘッダにページ番号を書く
        topic_page_nums[topic.get("topic")] = pm.get()  # 目次のためにページ番号を覚えておく

        # トピックのタイトルヘッダを作る
        topic_description = create_content(base_path, topic["path"], topic.get("description"), "トピック定義")
        rep_map = {"TITLE": topic.get("topic"), "DESCRIPTION": topic_description}
        topic_html += get_element("topic", rep_map)

        # ステップのコンテンツを並べる
        for num, step in enumerate(topic["steps"]):
            topic_html += pm.new_page()  # 改ページなら、ページヘッダにページ番号を書く

            # キャプション、テキスト、画像を入れる
            caption = step.get("caption", f"ステップ {num+1}")
            text = create_content(base_path, topic["path"], step, f"ステップ定義:{caption}")
            rep_map = {"IMAGE": get_image(base_path, topic["path"], step.get("image"), step.get("imgSize")),
                       "IMGSIZE": get_image_size(step.get("imgSize")),
                       "CAPTION": caption,
                       "TEXT": text}
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

