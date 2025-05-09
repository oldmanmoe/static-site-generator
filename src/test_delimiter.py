import unittest

from delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("Una prueba que tiene **ki.** Ve klk?", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Expected: 3 nodes with the bold part in the middle
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Una prueba que tiene ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "ki.")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " Ve klk?")
        self.assertEqual(result[2].text_type, TextType.TEXT)   
                         
    def test_delimiter_italic(self):
        node = TextNode("Un texto con _finura y elegancia._Ruede durisimo", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Un texto con ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "finura y elegancia.")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, "Ruede durisimo")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_delimiter_code(self):
        node = TextNode("Code example: `print('klk mi gente')` end.", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
 
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Code example: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "print('klk mi gente')")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " end.")
        self.assertEqual(result[2].text_type, TextType.TEXT)        
    