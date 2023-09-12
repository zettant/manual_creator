import copy
import os
import sys
import yaml
import glob
import shutil


TEMPLATE_DIR = os.path.dirname(__file__)


def _read_config(file_path: str) -> dict:
    if not os.path.exists(file_path):
        print("XXX no config.yml:", file_path)
        sys.exit(1)
    with open(file_path) as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    return conf


def walk_in_directory_to_create_conf(dir_path: str):
    """入力ディレクトリを走査して、マニュアルを作るためのコンフィグを作成する"""
    conf_path = os.path.join(dir_path, "config.yml")
    conf = _read_config(conf_path)
    conf["topics"] = []

    for p in glob.glob(os.path.join(dir_path, "*")):
        if not os.path.isdir(p): continue
        cp = os.path.join(p, "config.yml")
        page_conf = _read_config(cp)
        page_conf["path"] = os.path.relpath(p, dir_path)
        conf["topics"].append(page_conf)

    return conf


manual_config = {
    "issuer": "発行者名の名前に変えてください",
    "title": "このマニュアルのタイトルを書いてください",
    "sections": [{
        "title": "セクションにタイトルをつけてください",
        "topics": [],
    }],
}


def create_new_manual_directory(dir_path: str):
    if os.path.exists(dir_path):
        print("XXX already exists:", dir_path)
        sys.exit(1)
    os.mkdir(dir_path)
    with open(os.path.join(dir_path, "config.yml"), "w", encoding='utf-8') as f:
        yaml.dump(manual_config, f, allow_unicode=True)


topic_config = {
    "topic": "トピックのタイトル行に各内容を入れてください",
    "description": {
      "file": "description.html"
    },
    "keywords": [],  # キーワードがあれば
    "steps": [],     # ステップ情報がここに入る
}


def add_new_topic(dir_path: str, name: str):
    topic_path = os.path.join(dir_path, name)
    topic_config["topic"] = name
    with open(os.path.join(topic_path, "config.yml"), "w", encoding='utf-8') as f:
        yaml.dump(topic_config, f, allow_unicode=True)

    with open(os.path.join(topic_path, "description.html"), "w", encoding='utf-8') as f:
        f.write("<div>\n</div>\n")

    # マニュアル全体のコンフィグにページ情報を追加する。とりあえず最初のセクションの一番最後に追加するので、必要なら手動で場所を替えてもらう
    conf_path = os.path.join(dir_path, "config.yml")
    conf = _read_config(conf_path)
    conf.get("sections", [])
    if len(conf["sections"]) == 0:
        conf["sections"][0].append({"topics", [name]})
    else:
        conf["sections"][0].get("topics", []).append(name)

    with open(conf_path, "w", encoding='utf-8') as f:
        yaml.dump(conf, f, allow_unicode=True)


step_config = {
    "image": "step1.png",
    "imgSize": "1x1",
    "caption": "",
    "file": "step1.html",
    "keywords": [],   # キーワードがあれば書く
}


def add_new_step(dir_path: str):
    conf_path = os.path.join(dir_path, "config.yml")
    conf = _read_config(conf_path)
    new_conf = copy.deepcopy(step_config)

    # コンフィグのアップデート
    step = len(conf["steps"])+1
    new_conf["image"] = f"step{step}.png"
    new_conf["file"] = f"step{step}.html"
    conf["steps"].append(new_conf)
    with open(conf_path, "w", encoding='utf-8') as f:
        yaml.dump(conf, f, allow_unicode=True)

    # ファイル作成
    with open(os.path.join(dir_path, f"step{step}.html"), "w", encoding='utf-8') as f:
        f.write("<div>\n</div>\n")

    print(f"### step{step}.pngという名前で画像をこのディレクトリに置いてください。")
    print(f"### 大きさを変更したり、ファイル名を違うものにしたい場合は、config.ymlを編集してください。")
