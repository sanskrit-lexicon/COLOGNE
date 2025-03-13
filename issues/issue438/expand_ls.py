import re
import sys

def parse_ls_tags(input_string):
    def process_ls_tag(match):
        full_tag = match.group(0)
        content = match.group(1)
        
        prefix, data = content.split(". ", 1)
        prefix = prefix.strip() + "."  # Ensure period at the end of prefix
        entries = data.split(". ")
        
        prev_chapter, prev_section, prev_line = None, None, None
        output = []
        
        for item in entries:
            item = item.rstrip(".")  # Remove trailing period to avoid duplication
            parts = item.split(",")
            
            if len(parts) == 3:
                prev_chapter, prev_section, prev_line = parts
            elif len(parts) == 2:
                prev_section, prev_line = parts
            elif len(parts) == 1:
                prev_line = parts[0]
            else:
                continue
            
            id_value = f"{prev_chapter},{prev_section},{prev_line}" if prev_line else f"{prev_chapter},{prev_section}"
            output.append(f'<ls n="{prefix}" id="{id_value}">{item}.</ls>')
        
        return " ".join(output)
    
    return re.sub(r"<ls>(.*?)</ls>", process_ls_tag, input_string)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py '<ls>AK. 1,3,45. 46. 2,24. 3,4,56.</ls>'")
        sys.exit(1)
    
    input_string = sys.argv[1]
    print(parse_ls_tags(input_string))

