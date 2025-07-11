from textnode import TextNode, TextType
import re

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes         


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def find_delimiter_pairs(text, delimiter=delimiter):
        start_index  = text.find(delimiter)
        if start_index == -1:
            return None

        end_index = text.find(delimiter, start_index + len(delimiter))
        if end_index == -1:
            raise Exception(f"Closing delimiter {delimiter} not found")

        before_text = text[:start_index]
        delimiter_text = text[start_index + len(delimiter):end_index]
        after_text = text[end_index + len(delimiter):]

        return before_text, delimiter_text, after_text
    
    new_nodes = []
    for node in old_nodes: 
        if node.text_type == TextType.TEXT:
            result = find_delimiter_pairs(node.text)
            if result:
                before_text, delimiter_text, after_text = result
                new_nodes.append(TextNode(before_text, TextType.TEXT))
                new_nodes.append(TextNode(delimiter_text, text_type))
                new_nodes.append(TextNode(after_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)     
    return new_nodes       


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        node_text = node.text
        if node_text == "":
            continue
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        matches = extract_markdown_images(node_text)
        if matches == []:
            result.append(TextNode(node_text, TextType.TEXT))
            continue
        for link_text, url in matches:
            pattern = f"![{link_text}]({url})"
            before_text, node_text = node_text.split(pattern, 1)
            if before_text:
                result.append(TextNode(before_text, TextType.TEXT))
            result.append(TextNode(link_text, TextType.IMAGE, url))
        if node_text:
            result.append(TextNode(node_text, TextType.TEXT))
    return result
        

def split_nodes_link(old_nodes):
    result = [] 
    for node in old_nodes:
        node_text = node.text
        if node_text == "":
            continue
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        matches = extract_markdown_links(node_text)
        if matches == []:
            result.append(TextNode(node_text, TextType.TEXT))
            continue
        for display_text, url in matches:
            pattern = f"[{display_text}]({url})"
            before_text, node_text = node_text.split(pattern, 1)
            if before_text:
                result.append(TextNode(before_text, TextType.TEXT))
            result.append(TextNode(display_text, TextType.LINK, url))
        if node_text:
            result.append(TextNode(node_text, TextType.TEXT))
    return result


def extract_markdown_images(text):
    link_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches


def extract_markdown_links(text):
    image_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_matches





















