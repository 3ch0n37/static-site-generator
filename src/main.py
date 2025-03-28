#! /bin/env python3
import os
import shutil
from pathlib import Path
from site_generator import generate_page

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

def main():
    path = Path(__file__)
    root_dir = path.parent.parent.absolute()
    print(root_dir)
    public_dir = os.path.join(root_dir, 'public')
    static_dir = os.path.join(root_dir, 'static')
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir, ignore_errors=True)
    os.mkdir(public_dir)

    recursive_copy(static_dir, public_dir)

    template_file = os.path.join(root_dir, 'template.html')
    if not os.path.exists(template_file):
        raise ValueError(f"Template file does not exist")
    md_file = os.path.join(root_dir, 'content', 'index.md')
    if not os.path.exists(md_file):
        raise ValueError(f"Markdown file does not exist")
    result_file = os.path.join(public_dir, 'index.html')
    print(f"Generating page from {md_file} to {result_file} using {template_file}")
    generate_page(
        md_file,
        template_file,
        result_file
    )


if __name__ == '__main__':
    main()
