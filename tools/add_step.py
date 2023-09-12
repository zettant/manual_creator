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
from argparse import ArgumentParser

from libs.config_parse import walk_in_directory_to_create_conf, create_new_manual_directory, add_new_page
from libs.build_page import build


def _parser():
    usage = "python {} [-i input_directory] [-o output html file] [--help]".format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument("-i", "--input", type=str, help="directory path")
    argparser.add_argument("-o", "--output", type=str, default="manual.html", help="output file name")
    argparser.add_argument("--new", type=str, help="start new manual with directory name")
    argparser.add_argument("-a", "--add", type=str, help="add new page (-i is mandatory)")
    return argparser.parse_args()


if __name__ == '__main__':
    args = _parser()
    if args.new is not None:
        create_new_manual_directory(args.new)
        sys.exit(0)

    if not os.path.exists(args.input):
        print("XXX no such directory:", args.input)
        sys.exit(1)

    if args.add is not None:
        add_new_page(args.input, args.add)
        sys.exit(0)

    conf = walk_in_directory_to_create_conf(args.input)
    html = build(args.input, conf)

    with open(args.output, "w") as f:
        f.write(html)


