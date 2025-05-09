import unittest

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = "" 
        if self.props is not None:
            for k, v in self.props.items():
                k.replace('"', "")
                result += f' {k}="{v}"'
        return result
    

    def __repr__(self):
        return f"Tag:{self.tag}\n Value:{self.value}\n Children:{self.children}\n Props:{self.props}"
            
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        
        if self.tag is None:
            return f"{self.value}"
        
        props_html = ""
        if self.props:
            props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
   
 
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have children")
        
        html = f"<{self.tag}"
        if self.props:
            html += self.props_to_html()
        
        html += ">"
        for child in self.children:
            html += child.to_html() 
            
        html += f"</{self.tag}>"
        return html


    
        
        
        
        
        
        
        
        
        

if __name__ == "__main__":
    unittest.main()
        