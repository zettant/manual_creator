"""
*  [2023] Zettant Incorporated
*  All Rights Reserved.
*
* NOTICE:  All information contained herein is, and remains
* the property of Zettant Incorporated and its suppliers,
* if any.  The intellectual and technical concepts contained
* herein are proprietary to Zettant Incorporated and its
* suppliers and may be covered by Japan. and Foreign Patents,
* patents in process, and are protected by trade secret or
* copyright law. Dissemination of this information or
* reproduction of this material is strictly forbidden unless
* prior written permission is obtained from Zettant Incorporated.
"""

import os
import sys
import subprocess
from argparse import ArgumentParser

from libs.config_parse import add_new_topic


def _parser():
    usage = "python {} [-t topic_name] [-o output html file] [--help]".format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument("-t", "--topic", type=str, help="topic name to add")
    return argparser.parse_args()


if __name__ == '__main__':
    args = _parser()
    if args.topic is None:
        print("XXX -t is mandatory!")
        sys.exit(1)

    dir_path = os.path.dirname(__file__)
    topic_path = os.path.join(dir_path, args.topic)
    if os.path.exists(topic_path):
        print("XXX already exists:", args.topic)
        sys.exit(1)
    os.makedirs(topic_path, exist_ok=True)

    # ツールへのシンボリックリンクを作成
    tool_abs_dir = os.path.dirname(os.path.realpath(__file__))
    tool_dir = os.path.relpath(tool_abs_dir, topic_path)
    subprocess.run(f"ln -s {tool_dir}/add_step.py", shell=True, cwd=topic_path)

    # configの追加
    add_new_topic(".", args.topic)

    print("### トピックを作成するセクションは選べないので、意図通りではない場合は、config.ymlを直接編集してください。")
