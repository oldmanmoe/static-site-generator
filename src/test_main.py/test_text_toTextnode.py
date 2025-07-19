import unittest
from textnode import TextNode, TextType
from markdown_splitter import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is just plain text"
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        text = "This is **bold** text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_text(self):
        text = "This is _italic_ text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_text(self):
        text = "This is `code` text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "This is an ![image](https://example.com/image.png)"
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "This is a [link](https://example.com)"
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_combined_markdown(self):
        text = "This is **bold**, _italic_, `code`, ![image](https://i.imgur.com/zjjcJKZ.png), and [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(", and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


def test_multiple_images_and_links(self):
    text = "![first](img1.png) and ![second](img2.png) with [first link](url1) and [second link](url2)"
    expected = [
        TextNode("first", TextType.IMAGE, "img1.png"),
        TextNode(" and ", TextType.TEXT),
        TextNode("second", TextType.IMAGE, "img2.png"),
        TextNode(" with ", TextType.TEXT),
        TextNode("first link", TextType.LINK, "url1"),
        TextNode(" and ", TextType.TEXT),
        TextNode("second link", TextType.LINK, "url2"),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_bold_and_italic(self):
    text = "This is **bold** and _italic_ text"
    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" text", TextType.TEXT),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_bold_italic_and_code(self):
    text = "**Bold**, _italic_, and `code` in one sentence"
    expected = [
        TextNode("Bold", TextType.BOLD),
        TextNode(", ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(", and ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(" in one sentence", TextType.TEXT),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_image_with_adjacent_markdown(self):
    text = "Here's ![an image](img.png) with **bold** text"
    expected = [
        TextNode("Here's ", TextType.TEXT),
        TextNode("an image", TextType.IMAGE, "img.png"),
        TextNode(" with ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.TEXT),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_link_with_surrounding_markdown(self):
    text = "Click [here](url) for _important_ information"
    expected = [
        TextNode("Click ", TextType.TEXT),
        TextNode("here", TextType.LINK, "url"),
        TextNode(" for ", TextType.TEXT),
        TextNode("important", TextType.ITALIC),
        TextNode(" information", TextType.TEXT),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_all_types_combined(self):
    text = "**Bold**, _italic_, `code`, ![image](img.png), and [link](url)"
    expected = [
        TextNode("Bold", TextType.BOLD),
        TextNode(", ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(", ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(", ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "img.png"),
        TextNode(", and ", TextType.TEXT),
        TextNode("link", TextType.LINK, "url"),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_markdown_at_start_and_end(self):
    text = "**Bold** at start and _italic_ at end"
    expected = [
        TextNode("Bold", TextType.BOLD),
        TextNode(" at start and ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" at end", TextType.TEXT),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_multiple_instances_of_each_type(self):
    text = "**First** and **second** bold, _first_ and _second_ italic"
    expected = [
        TextNode("First", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("second", TextType.BOLD),
        TextNode(" bold, ", TextType.TEXT),
        TextNode("first", TextType.ITALIC),
        TextNode(" and ", TextType.TEXT),
        TextNode("second", TextType.ITALIC),
        TextNode(" italic", TextType.TEXT),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_code_with_other_markdown(self):
    text = "Use `print()` for **debugging** and _logging_"
    expected = [
        TextNode("Use ", TextType.TEXT),
        TextNode("print()", TextType.CODE),
        TextNode(" for ", TextType.TEXT),
        TextNode("debugging", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("logging", TextType.ITALIC),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_link_followed_by_image(self):
    text = "Visit [our site](url) and see ![our logo](logo.png)"
    expected = [
        TextNode("Visit ", TextType.TEXT),
        TextNode("our site", TextType.LINK, "url"),
        TextNode(" and see ", TextType.TEXT),
        TextNode("our logo", TextType.IMAGE, "logo.png"),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

def test_markdown_with_whitespace(self):
    text = "  **bold**  _italic_  `code`  "
    expected = [
        TextNode("  ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode("  ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode("  ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode("  ", TextType.TEXT),
    ]
    self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()