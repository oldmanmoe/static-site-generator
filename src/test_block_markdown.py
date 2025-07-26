
import unittest
from block_markdown import (
    markdown_to_html_node,
    BlockType,
    block_to_block_type,
    markdown_to_blocks
)
class TestBlockMarkdown(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- With items
"""
        new_md = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- With items"
        ]
        
        self.assertEqual(len(new_md), len(expected))
        for i in range(len(new_md)):
            self.assertEqual(new_md[i],expected[i])
            


    def test_extra_newlines(self):
        md = """
Header


Paragraph with extra gaps


- List item 1
- List item 2


Footer
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "Header",
            "Paragraph with extra gaps",
            "- List item 1\n- List item 2",
            "Footer"
        ]
        self.assertEqual(blocks, expected)
      
        
    def test_no_extra_newlines(self):
        md = "Single block with no newlines"
        blocks = markdown_to_blocks(md)
        expected = ["Single block with no newlines"]
        self.assertEqual(blocks, expected)


    def test_mixed_newlines(self):
        md = "Block 1\n\nBlock 2\nBlock 2 continued\n\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        expected = [
            "Block 1",
            "Block 2\nBlock 2 continued",
            "Block 3"
        ]
        self.assertEqual(blocks, expected)
        
    def test_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)
class TestBlockToBlockType(unittest.TestCase):
    def test_ordered_list(self):
        test_cases = [
            ("1. First item\n2. Second item\n3. Third item", BlockType.OLIST),
            ("1. Only one item", BlockType.OLIST),
            ("1. Item\n2. Item\n3. Item\n4. Item", BlockType.OLIST),
        ]

        for md_block, expected in test_cases:
            with self.subTest(md_block=md_block):
                self.assertEqual(block_to_block_type(md_block), expected)

    def test_invalid_ordered_list(self):
        test_cases = [
            ("1. First item\n3. Third item", BlockType.PARAGRAPH),  # Missing 2.
            ("2. Starts with wrong number", BlockType.PARAGRAPH),   # Should start with 1.
            ("1. Item\n2. Item\n4. Item", BlockType.PARAGRAPH),    # Skips 3.
        ]

        for md_block, expected in test_cases:
            with self.subTest(md_block=md_block):
                self.assertEqual(block_to_block_type(md_block), expected)
 # Heading Tests
    def test_heading_level1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
    
    def test_heading_level6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    
    def test_invalid_heading(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    # Code Block Tests
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
    
    def test_unclosed_code_block(self):
        self.assertEqual(block_to_block_type("```\nunclosed"), BlockType.PARAGRAPH)

    # Quote Tests
    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
    
    def test_multi_line_quote(self):
        text = """> Line 1
> Line 2
> Line 3"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_mixed_quote(self):
        text = """> Line 1
Not a quote
> Line 3"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

# Unordered List Tests
    def test_unordered_list(self):
        text = """- Item 1
- Item 2
- Item 3"""
        self.assertEqual(block_to_block_type(text), BlockType.ULIST)
    
    def test_invalid_unordered_list(self):
        text = """- Item 1
* Item 2"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    # Ordered List Tests
    def test_perfect_ordered_list(self):
        text = """1. First
2. Second
3. Third"""
        self.assertEqual(block_to_block_type(text), BlockType.OLIST)
    
    def test_broken_ordered_list(self):
        text = """1. First
3. Third"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_starting_non1_ordered_list(self):
        self.assertEqual(block_to_block_type("2. Second"), BlockType.PARAGRAPH)

# Paragraph Tests
    def test_regular_paragraph(self):
        self.assertEqual(block_to_block_type("Normal text"), BlockType.PARAGRAPH)
   
class TestMarkdownToHTML(unittest.TestCase):
    def test_empty_markdown(self):
        markdown = ""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 0)

    def test_single_paragraph(self):
        markdown = "This is a simple paragraph."
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].value, "This is a simple paragraph.")

    def test_paragraph_with_formatting(self):
        markdown = "This has **bold** and _italic_ text."
        result = markdown_to_html_node(markdown)
        p_node = result.children[0]
        self.assertEqual(p_node.tag, "p")
        self.assertEqual(len(p_node.children), 5)  # text, bold, text
        self.assertEqual(p_node.children[1].tag, "b")  # bold part

    def test_headings_all_levels(self):
        markdown = "# Heading 1\n## Heading 2\n### Heading 3"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "h2")
        self.assertEqual(result.children[2].tag, "h3")

    def test_code_block(self):
        markdown = "```\nprint('Hello World')\n```"
        result = markdown_to_html_node(markdown)
        pre_node = result.children[0]
        self.assertEqual(pre_node.tag, "pre")
        self.assertEqual(pre_node.children[0].tag, "code")
        self.assertIn("print('Hello World')", pre_node.children[0].value)

    def test_quote_block(self):
        markdown = "> This is a quote\n> spanning multiple lines"
        result = markdown_to_html_node(markdown)
        quote_node = result.children[0]
        self.assertEqual(quote_node.tag, "blockquote")
        self.assertIn("This is a quote", quote_node.children[0].value)
        self.assertIn("spanning multiple lines", quote_node.children[0].value)

    def test_unordered_list(self):
        markdown = "- Item 1\n- **Item** 2\n- Item 3"
        result = markdown_to_html_node(markdown)
        ul_node = result.children[0]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 3)
        self.assertEqual(ul_node.children[1].children[0].tag, "b")  # bold in item 2

    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        result = markdown_to_html_node(markdown)
        ol_node = result.children[0]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 3)
       

    def test_mixed_blocks(self):
        markdown = """# Header

This is a paragraph with **bold**.

- List item 1
- List item 2

```python
print('code')
```"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 4)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[2].tag, "ul")
        self.assertEqual(result.children[3].tag, "pre")

    def test_edge_case_whitespace(self):
        markdown = "   \n\n  # Heading with spaces  \n  \n"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "h1")

    def test_inline_code_in_paragraph(self):
        markdown = "This has `inline code` in it."
        result = markdown_to_html_node(markdown)
        p_node = result.children[0]
        self.assertEqual(p_node.children[1].tag, "code")
        self.assertEqual(p_node.children[1].value, "inline code") 
    
if __name__ == "__main__":
    unittest.main()