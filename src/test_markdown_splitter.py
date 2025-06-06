import unittest
from textnode import TextNode, TextType
from markdown_splitter import split_nodes_link,split_nodes_image

class TestTextSplitter(unittest.TestCase):
    def test_split_nodes_link_single(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) in it.", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" in it.", TextType.TEXT),
            ]
        
        self.assertEqual(len(new_nodes), len(expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, expected[i].text)
            self.assertEqual(new_nodes[i].text_type, expected[i].text_type)
            self.assertEqual(new_nodes[i].url, expected[i].url)
        
    def test_split_nodes_image_single(self):
        node = TextNode(
            "Esto es un texto con una imagen de ursula ![munki](https://shorturl.at/dHxeL) le llega??", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("Esto es un texto con una imagen de ursula ", TextType.TEXT),
            TextNode("munki", TextType.IMAGE, "https://shorturl.at/dHxeL"),
            TextNode(" le llega??", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), len(expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, expected[i].text)
            self.assertEqual(new_nodes[i].text_type, expected[i].text_type)
            self.assertEqual(new_nodes[i].url, expected[i].url)
            
    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "Check out [this](https://example.com) and [that](https://example.org) for more info.",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("this", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("that", TextType.LINK, "https://example.org"),
            TextNode(" for more info.", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), len(expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, expected[i].text)
            self.assertEqual(new_nodes[i].text_type, expected[i].text_type)
            self.assertEqual(new_nodes[i].url, expected[i].url)


    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "First image: ![alt1](img1.png), second: ![alt2](img2.jpg).",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("First image: ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "img1.png"),
            TextNode(", second: ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "img2.jpg"),
            TextNode(".", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), len(expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, expected[i].text)
            self.assertEqual(new_nodes[i].text_type, expected[i].text_type)
            self.assertEqual(new_nodes[i].url, expected[i].url)
            

    def test_split_nodes_link_empty_text(self):
        # Empty text node should result in empty list
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])

    def test_split_nodes_image_empty_text(self):
        # Empty text node should result in empty list
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [])

    def test_split_nodes_link_only_link(self):
        # Text is JUST a link (no surrounding text)
        node = TextNode("[link](https://lonk.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("link", TextType.LINK, "https://lonk.com")]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_only_image(self):
        # Text is JUST an image (no surrounding text)
        node = TextNode("![image](https://imgur.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("image", TextType.IMAGE, "https://imgur.com")]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_whitespace(self):
        # Edge case: link surrounded by whitespace
        node = TextNode("   [whitespace](https://whitespace.com)   ", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("   ", TextType.TEXT),
            TextNode("whitespace", TextType.LINK, "https://whitespace.com"),
            TextNode("   ", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_whitespace(self):
        # Edge case: image surrounded by whitespace
        node = TextNode("   ![whitespace](image.png)   ", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("   ", TextType.TEXT),
            TextNode("whitespace", TextType.IMAGE, "image.png"),
            TextNode("   ", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)