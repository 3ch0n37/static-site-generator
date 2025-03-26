def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise ValueError("Invalid markdown, not string.")
    markdown = markdown.strip()
    return [section.strip() for section in markdown.split("\n\n") if section.strip()]