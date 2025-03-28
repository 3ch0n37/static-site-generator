import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    sections =  markdown.split('\n')
    if len(sections) < 2 or not sections[0].startswith('# '):
        raise Exception('Markdown file must have a title')
    return sections[0].replace('# ', '')

def generate_page(from_path, template_path, dest_path):
    with open(from_path, 'r') as f:
        markdown = f.read()
    title = extract_title(markdown)

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    with open(template_path, 'r') as f:
        template = f.read()
    page = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    with open(dest_path, 'w') as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, item)
        if os.path.isdir(path):
            new_dir = os.path.join(dest_dir_path, item)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            generate_pages_recursive(path, template_path, new_dir)
        else:
            if item.endswith('.md'):
                dest_path = os.path.join(dest_dir_path, item.replace('.md', '.html'))
                generate_page(path, template_path, dest_path)