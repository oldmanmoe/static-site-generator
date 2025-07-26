import unittest
from markdown_splitter import text_to_textnodes
from textnode import TextNode, TextType

class TestTextToNodes(unittest.TestCase):
    
    def test_text_to_nodes(self):
        text = "This is a **test** to see if _my program_ is `running` correctly [bootdev](www.boot.dev) here is a koala ![koala](www.koala.com) enjoy!"
        
        new_nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.BOLD),
            TextNode(" to see if ", TextType.TEXT),
            TextNode("my program", TextType.ITALIC),
            TextNode(" is ", TextType.TEXT),
            TextNode("running", TextType.CODE),
            TextNode(" correctly ", TextType.TEXT),
            TextNode("bootdev", TextType.LINK, "www.boot.dev"),
            TextNode(" here is a koala ", TextType.TEXT),
            TextNode("koala", TextType.IMAGE, "www.koala.com"),
            TextNode(" enjoy!", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), len(expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, expected[i].text)
            self.assertEqual(new_nodes[i].text_type, expected[i].text_type)
            self.assertEqual(new_nodes[i].url, expected[i].url)
    
    def test_empty_text(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [])
    
    def test_only_text(self):
        text = "Just plain text without any markdown"
        new_nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text without any markdown", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    
    def test_nested_markdown(self):
        text = "Text with **bold _and italic_** inside"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold _and italic_", TextType.BOLD),
            TextNode(" inside", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, expected[i].text)
            self.assertEqual(new_nodes[i].text_type, expected[i].text_type)
    
    def test_adjacent_markdown(self):
        text = "**bold**_italic_`code`"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(len(new_nodes), len(expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, expected[i].text)
            self.assertEqual(new_nodes[i].text_type, expected[i].text_type)
        