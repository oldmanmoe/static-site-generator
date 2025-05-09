import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_properties(self):
        node = HTMLNode("h1","Watagapitusberry", None, {"href": "https://www.google.com","target": "_blank",} )
        expected = ' href="https://www.google.com" target="_blank"'
        
        self.assertEqual(node.props_to_html(), expected)        
        
    def test_props_to_html_no_properties(self):
        node2 = HTMLNode(None, None, None, None)
        expected2 = ""
        
        self.assertEqual(node2.props_to_html(), expected2)
        
    def test_repr_with_properties(self):
        node = HTMLNode("div", "klk tu dice palomo", None, {"class": "container"})
        node3 = HTMLNode("head", None, None, {"": ""})
        repr_str = repr(node)
        repr_str3 = repr(node3)    
        
        self.assertIn("div", repr_str)
        self.assertIn("klk tu dice palomo", repr_str)
        self.assertIn("class", repr_str)
        self.assertIn("container", repr_str)
        self.assertIn("head", repr_str3)
        self.assertIn("", repr_str3)
    
    def test_repr_with_no_properties(self):
        
        node2 = HTMLNode(None, None, None, None)
        repr_str2 = repr(node2) 
        
        self.assertIn("None", repr_str2)
       
    def test_to_html_p_with_properties(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode(None, "KLK")
        
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "KLK")
        

    def test_to_html_p_all_properties(self):
        node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        
        self.assertEqual(node3.to_html(), '<a href="https://www.google.com">Click me!</a>')

        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
        
    def test_to_html_with_children_props(self):
        grandchild_node = LeafNode("head", "KLK")
        child_node = ParentNode("b", [grandchild_node], {"href": "https://www.google.com"})
        self.assertEqual(child_node.to_html(), '<b href="https://www.google.com"><head>KLK</head></b>')
    
    def test_to_html_no_properties(self):
        grandchild_node = LeafNode("b","tu no mete cabra sarabambiche")
        child_node = ParentNode("div", None, {"href": "https://www.google.com"})
        child_node2 = ParentNode(None,[grandchild_node])
        self.assertRaises(ValueError,child_node.to_html)
        self.assertRaises(ValueError, child_node2.to_html)
        
    def test_to_html_with_deep_nesting(self):
        great_grandchild = LeafNode("a", "link", {"href": "/example"})
        grandchild = ParentNode("b", [great_grandchild])
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(),'<div><span><b><a href="/example">link</a></b></span></div>',)
        
    def test_to_html_with_mixed_children(self):
        leaf_child = LeafNode("p", "Hello")
        parent_child = ParentNode("div", [LeafNode("span", "nested")])
        parent_node = ParentNode("section", [leaf_child, parent_child])
        self.assertEqual(parent_node.to_html(),"<section><p>Hello</p><div><span>nested</span></div></section>",)
        
    def test_to_html_with_text_only_leaf(self):
        text_node = LeafNode(None, "Raw text")
        parent_node = ParentNode("div", [text_node])
        self.assertEqual(parent_node.to_html(), "<div>Raw text</div>")
        
  