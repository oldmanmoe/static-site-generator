import re

def extract_markdown_images(text):
    link_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches

def extract_markdown_links(text):
    image_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_matches

