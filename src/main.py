import os
import shutil
from pathlib import Path
from htmlnode import *
from block_markdown import markdown_to_html_node



def main():    

    
    find_files("/Users/moisesangeles/workspace/github.com/oldmanmoe/static-site-generator/static",
               "/Users/moisesangeles/workspace/github.com/oldmanmoe/static-site-generator/public")
    
    generate_page("/Users/moisesangeles/workspace/github.com/oldmanmoe/static-site-generator/content/index.md",
                  "/Users/moisesangeles/workspace/github.com/oldmanmoe/static-site-generator/template.html",
                  "/Users/moisesangeles/workspace/github.com/oldmanmoe/static-site-generator/public")
        

def find_files(src_path, dest_path, file_log=None):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
        if os.path.isfile(dest_path):
            shutil.copy(src_path,dest_path)
        else:
            os.mkdir(dest_path)
            
    if file_log is None:
        file_log = []
    
    if os.path.exists(src_path):
        if os.path.isfile(src_path):
            file_log.append(src_path)
        else:
            src_list = os.listdir(src_path)
            for file in src_list:
                new_src_path = os.path.join(src_path, file)
                new_dest_path = os.path.join(dest_path, file)
                if os.path.isfile(new_src_path):
                    file_log.append(new_src_path)
                    shutil.copy(new_src_path,new_dest_path)
                else:
                    os.mkdir(new_dest_path)
                    find_files(new_src_path, new_dest_path, file_log)
   
def extract_title(markdown):
    lines = markdown.split("\n")
    found = False
    while found == False:
        for line in lines:
            if line.startswith("# "):
                title = line.strip("# ")
                found = True
                return title
        if not found:
            raise Exception("Title not found: Missing #")
    
def generate_page(from_path, template_path, dest_path):
    print(f"\n\nGenerating path from {from_path} to {dest_path} using {template_path}")
    
    from_path = Path(from_path)
    template_path = Path(template_path)
    dest_path = Path(dest_path)
    
    with open(from_path, 'r') as fpath_file:
        fpath_content = fpath_file.read()
    
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
             
    fpath_html = markdown_to_html_node(fpath_content).to_html()
    fpath_title = extract_title(fpath_content)
    
    output = template_content.replace("{{ Title }}", fpath_title).replace("{{ Content }}", fpath_html) 
    
    if dest_path.is_dir():
        dest_path = dest_path / "index.html"
 
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, 'w') as dest_file:
        dest_file.write(output)
    
if __name__ == "__main__":
    main()