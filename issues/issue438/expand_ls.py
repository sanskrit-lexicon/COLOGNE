import re
import sys

def parse_ls_tags(input_string):
    prev_prefix = None  # Store previously seen book name
    
    def process_ls_tag(match):
        nonlocal prev_prefix
        full_tag = match.group(0)
        content = match.group(1)
        
        if ". " not in content:
            return full_tag  # Return the original tag if no period is found
        
        parts = content.split(". ", 1)
        
        if len(parts) == 2:
            prefix, data = parts
            prefix = prefix.strip() + "."  # Ensure period at the end of prefix
            prev_prefix = prefix  # Update previous book name
        else:
            data = parts[0]
            if prev_prefix is None:
                return full_tag  # If no previous prefix exists, return as is
            prefix = prev_prefix
        
        entries = data.split(". ")
        prev_volume, prev_chapter, prev_section, prev_line = None, None, None, None
        output = []
        
        for item in entries:
            item = item.rstrip(".")  # Remove trailing period to avoid duplication
            parts = item.split(",")
            
            if len(parts) == 4:
                prev_volume, prev_chapter, prev_section, prev_line = parts
            elif len(parts) == 3:
                prev_chapter, prev_section, prev_line = parts
            elif len(parts) == 2:
                prev_section, prev_line = parts
            elif len(parts) == 1:
                prev_line = parts[0]
            else:
                continue
            
            id_value = f"{prev_volume},{prev_chapter},{prev_section},{prev_line}" if prev_volume else f"{prev_chapter},{prev_section},{prev_line}"
            output.append(f'<ls n="{prefix}" id="{id_value}">{item}.</ls>')
        
        return " ".join(output)
    
    return re.sub(r"<ls>(.*?)</ls>", process_ls_tag, input_string)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        prev_prefix = None  # Store previous book name across lines
        
        for line in infile:
            line = re.sub("<ls n=\"[^>]*\">", "<ls>", line)  # Remove existing n attributes
            processed_line = parse_ls_tags(line)
            outfile.write(processed_line + "\n")
