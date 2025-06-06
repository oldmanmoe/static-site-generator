

def markdown_to_blocks(markdown):
    md_split = markdown.split('\n\n')
    result = []
    for sentence in md_split:
        clean_sentence = sentence.strip('\n')
        result.append(clean_sentence)
        
    return result
    
    
    
  