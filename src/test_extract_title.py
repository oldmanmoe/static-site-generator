import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_single_title(self):
        """Test extracting a single title at the start"""
        markdown = "# My Title\nSome content here"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_not_first_line(self):
        """Test title appears after some content"""
        markdown = "Some intro\n# The Actual Title\nMore content"
        self.assertEqual(extract_title(markdown), "The Actual Title")

    def test_multiple_h1s(self):
        """Test only the first H1 is returned"""
        markdown = "# First Title\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_no_title(self):
        """Test exception when no title exists"""
        markdown = "No title here\nJust content"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Title not found: Missing #")

    def test_empty_string(self):
        """Test empty input string"""
        with self.assertRaises(Exception) as context:
            extract_title("")
        self.assertEqual(str(context.exception), "Title not found: Missing #")

    def test_only_whitespace(self):
        """Test input with only whitespace"""
        with self.assertRaises(Exception) as context:
            extract_title("   \n  \t\n ")
        self.assertEqual(str(context.exception), "Title not found: Missing #")

    def test_title_with_special_chars(self):
        """Test title with special characters"""
        markdown = "# Title: With $pecial Ch@racter$!"
        self.assertEqual(extract_title(markdown), "Title: With $pecial Ch@racter$!")

if __name__ == '__main__':
    unittest.main()
    
    
    