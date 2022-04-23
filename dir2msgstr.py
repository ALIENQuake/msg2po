#!/usr/bin/env python3
# coding: utf-8

import os
import argparse
import re
from bgforge_po import cd, get_ext, get_enc, file2msgstr, po_make_unique, CONFIG
from polib import pofile, POFile

# parse args
parser = argparse.ArgumentParser(
    description="Load strings from files in selected dir into PO msgstr's",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("-s", dest="src_dir", default=".", help="directory to load", required=True)
parser.add_argument("-o", dest="output_file", help="existing PO file", required=True)
parser.add_argument("--ext", dest="file_ext", help="load files with this extension", required=True)
parser.add_argument(
    "--overwrite", dest="overwrite", default=False, action="store_true", help="overwrite existing msgstrs"
)
parser.add_argument(
    "--same",
    dest="same",
    default=False,
    action="store_true",
    help="load translations that are identical to original strings",
)
args = parser.parse_args()

# init vars
src_dir = args.src_dir
ext = args.file_ext
output_file = args.output_file
overwrite = args.overwrite

devnull = open(os.devnull, "w")


def dir2msgstr(src_dir: str, po: POFile, overwrite: bool = True):
    """
    src_dir is relative
    overwrite means ovewrite existing entries if any
    """
    print("overwrite is " + str(overwrite))
    with cd(src_dir):

        for dir_name, subdir_list, file_list in os.walk(".", topdown=False, followlinks=True):
            for file_name in file_list:
                full_name = os.path.join(dir_name, file_name)
                full_name = re.sub("^\./", "", full_name)  # remove trailing './'
                fext = get_ext(file_name)
                if not fext == ext:
                    continue
                # if CONFIG.extract_format == "sfall":
                if dir_name.endswith(CONFIG.female_dir_suffix):
                    print("{} is a file with female strings, skipping".format(full_name))
                    continue

                enc = get_enc(src_dir, file_name)
                print("processing {} with encoding {}".format(full_name, enc))
                po = file2msgstr(full_name, po, full_name, enc, overwrite, args.same)
    po = po_make_unique(po)
    return po


po = pofile(output_file)
po = dir2msgstr(src_dir, po, overwrite)

po.save(output_file, newline=CONFIG.newline)
print("Processed directory {}, the result is in {}".format(src_dir, output_file))
