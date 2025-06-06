
import unittest
from block_markdown import markdown_to_blocks

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
        expected = ['']
        self.assertEqual(blocks, expected)


            
if __name__ == "__main__":
    unittest.main()