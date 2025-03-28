#! /bin/env python3
import os
import shutil
import sys
from pathlib import Path

from mercurial.wireprotoframing import outputstream

from site_generator import generate_page, generate_pages_recursive

def recursive_copy(src, dest):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            print(f"copying directory {s} to {d}")
            os.mkdir(d)
            recursive_copy(s, d)
        else:
            print(f"copying file {s} to {d}")
            shutil.copy(s, d)

def main(basepath = "/"):
    path = Path(__file__)
    root_dir = path.parent.parent.absolute()
    print(root_dir)
    output_dir = os.path.join(root_dir, 'docs')
    static_dir = os.path.join(root_dir, 'static')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)
    os.mkdir(output_dir)

    recursive_copy(static_dir, output_dir)

    template_file = os.path.join(root_dir, 'template.html')
    if not os.path.exists(template_file):
        raise ValueError(f"Template file does not exist")
    content_dir = os.path.join(root_dir, 'content')

    generate_pages_recursive(content_dir, template_file, output_dir, basepath)


if __name__ == '__main__':
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    main(basepath)
