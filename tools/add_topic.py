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

from libs.config_parse import walk_in_directory_to_create_conf, create_new_manual_directory, add_new_page
from libs.build_page import build


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
    os.makedirs(topic_path, exist_ok=True)

    # ツールへのシンボリックリンクを作成
    tool_abs_dir = os.path.dirname(os.path.realpath(__file__))
    tool_dir = os.path.relpath(tool_abs_dir, topic_path)
    subprocess.run(f"ln -s {tool_dir}/add_step.py", shell=True, cwd=topic_path)

