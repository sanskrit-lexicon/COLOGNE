import sys
import re

def preprocess_ls_tags(content):
    """Removes <is> tags inside <ls> tags."""
    return re.sub(r'<ls>(MED\. )<is>(.*?)</is>', r'<ls>\1\2', content)

def medini(ls_content):
    """Handles special ls tags transformation for MED. references."""
    return re.sub(r'<ls>(MED\.)\s+(\S+)\.\s*(\d+)\.?<\/ls>',
                  r'<ls n="\1" id="\2,\3">\1 \2. \3.</ls>',
                  ls_content)

def verzdoxf(ls_content):
    """Handles special ls tags transformation for Verz. d. Oxf. H. references."""
    return re.sub(r'<ls>(Verz\. d\. Oxf\. H\.)\s+([0-9]+,[ab],[0-9]+\.)<\/ls>',
                  r'<ls n="\1" id="\2">\1 \2</ls>',
                  ls_content)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, "r", encoding="utf-8") as infile:
        content = infile.read()
    
    content = preprocess_ls_tags(content)
    content = medini(content)
    transformed_content = verzdoxf(content)
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(transformed_content)
