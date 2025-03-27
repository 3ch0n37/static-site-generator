from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise ValueError("Invalid markdown, not string.")
    markdown = markdown.strip()
    return [section.strip() for section in markdown.split("\n\n") if section.strip()]

def is_heading(heading):
    return heading.startswith('# ') and len(heading.split("\n")) == 1

def is_unordered_list(block):
    for line in block.split("\n"):
        if not line.startswith("- "):
            return False
    return True

def is_ordered_list(block):
    lines = block.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            return False
    return True

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
