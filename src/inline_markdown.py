import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, delimited section not closed.")
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    # pattern = r"!\[(.*)\]\((.*)\)"
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # pattern = r"\[(.*)\]\((.*)\)"
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_link_image(old_nodes, is_image, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        elements = []
        node_text = old_node.text
        if is_image:
            elements = extract_markdown_images(node_text)
        else:
            elements = extract_markdown_links(node_text)
        for element in elements:
            [before, after] = node_text.split(f'{'!' if is_image else ''}[{element[0]}]({element[1]})', 1)
            if len(before) > 0:
                split_nodes.append(TextNode(before, TextType.TEXT))
            split_nodes.append(TextNode(element[0], text_type, element[1]))
            node_text = after
        if len(node_text):
            split_nodes.append(TextNode(node_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_link_image(old_nodes, True, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_link_image(old_nodes, False, TextType.LINK)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
