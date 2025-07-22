from textnode import *
import os
import shutil
def main():    
    not NotImplementedError

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
    
    
    
    
     
                
    
    



find_files("/Users/moisesangeles/workspace/github.com/oldmanmoe/static-site-generator/static",
           "/Users/moisesangeles/workspace/github.com/oldmanmoe/static-site-generator/public")
        
        
                
                
            
    
    
    
     

    
if __name__ == "__main__":
    main()