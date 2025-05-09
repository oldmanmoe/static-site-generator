import unittest

from textnode import TextNode, TextType, text_node_to_html_node



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a DIFFERENT text node", TextType.TEXT)
        node3 = TextNode("Different Text Node here", TextType.CODE, url="boot.dev")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node,node3)
        self.assertNotEqual(node2, node3)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
        node2 = TextNode("Texto con ki 10,000", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "Texto con ki 10,000")
        node4 = TextNode("pseudo code", TextType.CODE)
        html_node4 = text_node_to_html_node(node4)
        self.assertEqual(html_node4.tag, "code")
        
        node5 = TextNode("Un link a google", TextType.LINK, "https://google.com")
        html_node5 = text_node_to_html_node(node5)
        self.assertEqual(html_node5.tag, "a")
        self.assertEqual(html_node5.props,{'href': 'https://google.com'})
        
    def test_text_no_properties(self):
        node = TextNode("klk", 99)
        self.assertRaises(Exception,text_node_to_html_node, node)
        
        node2 = TextNode("brapp", None) 
        self.assertRaises(Exception, text_node_to_html_node, node2)
        
        node3 = TextNode("Claro que si", "Claro que entro")
        self.assertRaises(Exception,text_node_to_html_node, node3)
         
        node3 = TextNode("Vainita fina", TextType.ITALIC)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag, "i")
        
    def test_image_variations(self):
        # Test normal image
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://example.com/image.png','alt': 'Alt text'})        
        
        
if __name__ == "__main__":
    unittest.main()