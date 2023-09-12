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


def create_new_manual_directory(dir_path: str):
    if os.path.exists(dir_path):
        print("XXX already exists:", dir_path)
        sys.exit(1)
    os.mkdir(dir_path)
    shutil.copy(os.path.join(TEMPLATE_DIR, "templates/config/_main_config.yml"),
                os.path.join(dir_path, "config.yml"))


def add_new_page(dir_path: str, name: str):
    page_path = os.path.join(dir_path, name)
    if os.path.exists(page_path):
        print("XXX page already exists:", page_path)
        sys.exit(1)
    os.mkdir(page_path)
    shutil.copy(os.path.join(TEMPLATE_DIR, "templates/config/_page_config.yml"),
                os.path.join(page_path, "config.yml"))

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
