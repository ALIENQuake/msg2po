#!/usr/bin/env python3
# coding: utf-8


import argparse
from bgforge_po import po2file
from polib import POFile

parser = argparse.ArgumentParser(
    description="Extract WeiDU TRA from gettext PO", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("INPUT_FILE", help="input PO file")
parser.add_argument("OUTPUT_FILE", help="output TRA file")
parser.add_argument("-e", dest="encoding", help="output TRA encoding", default="cp1252")
parser.add_argument("--path", dest="path", help="TRA occurrence in PO (relative path) - defaults to output TRA name")
args = parser.parse_args()

if args.path is None:
    path = args.OUTPUT_FILE
else:
    path = args.path

po = POFile(args.INPUT_FILE)  # open once, it's a heavy op
po2file(po, args.OUTPUT_FILE, args.encoding, path)
