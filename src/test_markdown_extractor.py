import unittest
from markdown_extractor import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        text = "![alt text](image.png)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "image.png")])
        
        text = "![alt1](img1.png) and ![alt2](img2.jpg)"
        self.assertEqual(extract_markdown_images(text), 
                         [("alt1", "img1.png"), ("alt2", "img2.jpg")])
        
        text = "![](image.png)"
        self.assertEqual(extract_markdown_images(text), [("", "image.png")])
        
        text = "Just regular text"
        self.assertEqual(extract_markdown_images(text), [])
        
        text = "![alt-text_with.symbols](path/image-1.png)"
        self.assertEqual(extract_markdown_images(text), 
                         [("alt-text_with.symbols", "path/image-1.png")])
        
        text = """First line
        ![alt](img.png)
        Last line"""
        self.assertEqual(extract_markdown_images(text), [("alt", "img.png")])
    
    def test_extract_markdown_links(self):
        text = "[link text](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("link text", "https://example.com")])
        
        text = "[link1](url1) and [link2](url2)"
        self.assertEqual(extract_markdown_links(text), 
                         [("link1", "url1"), ("link2", "url2")])
        
        
        text = "[](https://empty.com)"
        self.assertEqual(extract_markdown_links(text), [("", "https://empty.com")])
        
        text = "Just regular text"
        self.assertEqual(extract_markdown_links(text), [])
        
        text = "[link-text_with.symbols](https://example.com/path?query=1)"
        self.assertEqual(extract_markdown_links(text), 
                         [("link-text_with.symbols", "https://example.com/path?query=1")])
        
        text = """First line
        [link](url)
        Last line"""
        self.assertEqual(extract_markdown_links(text), [("link", "url")])
        
        text = "![image](img.png) and [link](url)"
        self.assertEqual(extract_markdown_links(text), [("link", "url")])
    
    def test_no_false_positives(self):
        text = "![image](img.png) [link](url)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertEqual(images, [("image", "img.png")])
        self.assertEqual(links, [("link", "url")])
        
        text = "[malformed link(url) or ![malformed image]img.png)"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])
        
        text = "![should not match](image.png)"
        self.assertEqual(extract_markdown_links(text), [])
        
        text = "[should not match](url)"
        self.assertEqual(extract_markdown_images(text), [])

if __name__ == '__main__':
    unittest.main()
