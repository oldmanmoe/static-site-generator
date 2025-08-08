from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
from markdown_splitter import text_to_textnodes


def text_to_children(text, forced_tag=None):
    result = []

    if forced_tag is not None:
        split_text = text.split("\n")
        for single_text in split_text:
            if single_text.strip(): 
                text_nodes = text_to_textnodes(single_text)
                html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                if len(html_nodes) > 1:
                    children_nodes = []
                    for node in html_nodes:
                        children_nodes.append(node)
                    parent_node = ParentNode(forced_tag, children_nodes)
                    result.append(parent_node)
                else:
                    result.append(LeafNode(forced_tag, html_nodes[0].value))
    else:
        text_nodes = text_to_textnodes(text)
        for node in text_nodes:
            result.append(text_node_to_html_node(node))

    return result

def markdown_to_blocks(markdown):
    blocks = []
    current_block = []
    lines = markdown.split('\n')
    in_code_block = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith('```') and not in_code_block:
            if current_block:
                block_text = '\n'.join(current_block).strip()
                if block_text:
                    blocks.append(block_text)
                current_block = []
            
            in_code_block = True
            current_block.append(line)
        
        elif line.strip().startswith('```') and in_code_block:
            current_block.append(line)
            block_text = '\n'.join(current_block).strip()
            if block_text:
                blocks.append(block_text)
            current_block = []
            in_code_block = False
        
        elif in_code_block:
            current_block.append(line)
        
        else:
            if line.strip() == '':
                if current_block:
                    block_text = '\n'.join(current_block).strip()
                    if block_text:
                        blocks.append(block_text)
                    current_block = []
            else:
                current_block.append(line)
        
        i += 1
    
    if current_block:
        block_text = '\n'.join(current_block).strip()
        if block_text:
            blocks.append(block_text)
    
    return blocks
        
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"
    
def block_to_block_type(block):
    lines = [line.strip() for line in block.split("\n") if line.strip()]
    
    if not lines:
        return BlockType.PARAGRAPH
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")) for line in lines):
        return BlockType.HEADING
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    if len(lines) > 0:
        is_ordered = True
        for i, line in enumerate(lines, start=1):
            if not line.startswith(f"{i}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.OLIST
    
    return BlockType.PARAGRAPH

def process_heading_block(block):
    nodes = []
    for line in block.split("\n"):
        line = line.strip()
        if not line:
            continue
        node = process_heading_line(line)
        if node:
            nodes.append(node)
    return nodes
    
def process_heading_line(line):
    line = line.strip()
    if line.startswith("# "):
        return LeafNode("h1", line[2:])
    elif line.startswith("## "):
        return LeafNode("h2", line[3:])
    elif line.startswith("### "):
        return LeafNode("h3", line[4:])
    elif line.startswith("#### "):
        return LeafNode("h4", line[5:])
    elif line.startswith("##### "):
        return LeafNode("h5", line[6:])
    elif line.startswith("###### "):
        return LeafNode("h6", line[7:])
    return None
    


def strip_code_block(block):
    if block.startswith("```") and block.endswith("```"):
        block = block[3:-3].strip()
        lines = block.split('\n')
        if lines and lines[0].strip() and ' ' not in lines[0].strip():
            block = '\n'.join(lines[1:])
    return block
          
def strip_quote_prefix(block):
    lines = block.split("\n")
    tag = ""
    content_lines = []
    i = 1  
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if line.startswith("> "):
            content_lines.append(line[2:])
        else:
            content_lines.append(line) 
    
    content = "\n".join(content_lines)
    return content     


def process_list_block(block, list_type="ul"):
    """Process a list block and return proper list items"""
    lines = block.split("\n")
    list_items = []
    
    i = 1  # For ordered lists
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
            
        if list_type == "ul" and line.startswith("- "):
            # Extract content after "- "
            item_content = line[2:]
            # Process the content for inline markdown (images, links, etc.)
            item_children = text_to_children(item_content)
            list_items.append(ParentNode("li", item_children))
            
        elif list_type == "ol" and line.startswith(f"{i}. "):
            # Extract content after "1. ", "2. ", etc.
            item_content = line[len(f"{i}. "):]
            # Process the content for inline markdown (images, links, etc.)
            item_children = text_to_children(item_content)
            list_items.append(ParentNode("li", item_children))
            i += 1
    
    return list_items     

def markdown_to_html_node(markdown):
    children_nodes = []
    md = markdown_to_blocks(markdown)
    for block in md:
        block_copy = block[:]
        block_type = block_to_block_type(block_copy)
        
        if block_type == BlockType.PARAGRAPH:
            paragraph_child = text_to_children(block_copy)
            paragraph_parent = ParentNode("p", paragraph_child)
            children_nodes.append(paragraph_parent)
            
        if block_type == BlockType.HEADING:
            children_nodes.extend(process_heading_block(block))
    
        if block_type == BlockType.CODE:
            code_text = strip_code_block(block_copy)
            code_node = LeafNode("code", code_text)
            code_parent = ParentNode("pre", [code_node]) 
            children_nodes.append(code_parent) 
        
        if block_type == BlockType.QUOTE:
            quote_content = strip_quote_prefix(block_copy) 
            quote_child = text_to_children(quote_content) 
            quote_parent = ParentNode("blockquote", quote_child)
            children_nodes.append(quote_parent)
       
        if block_type == BlockType.ULIST:
            list_items = process_list_block(block_copy, "ul")
            ulist_parent = ParentNode("ul", list_items)
            children_nodes.append(ulist_parent)
        
        if block_type == BlockType.OLIST:
            list_items = process_list_block(block_copy, "ol")
            olist_parent = ParentNode("ol", list_items)
            children_nodes.append(olist_parent)
           
    return ParentNode("div", children_nodes)

