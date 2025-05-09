from textnode import TextNode, TextType

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