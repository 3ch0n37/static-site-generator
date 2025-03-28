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