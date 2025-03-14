import re
import sys

def reverse_transform_ls_tags(line):
    """
    Reverse transforms a line according to the rules:
    
    1. If an <ls> tag does NOT have an id attribute, it is preserved exactly.
    2. If an <ls> tag has an id attribute and its inner text is only digits, commas, periods (and whitespace),
       then remove the <ls> tag entirely and output just the inner text.
    3. If an <ls> tag has an id attribute and its inner text contains other characters,
       then remove all attributes but keep the tag (i.e. output <ls>inner text</ls>).
    
    Additionally, consecutive transformed <ls> tags (with id attribute) that are separated only by whitespace
    are merged into a single <ls>…</ls> group.
    """
    output = ""
    last_end = 0
    active_group = None  # If not None, a dict with keys: 'text' and 'group_n'
    
    # Pattern to match any <ls ...>...</ls> (non-greedy)
    pattern = re.compile(r'<ls(?P<attrs>[^>]*)>(?P<content>.*?)</ls>', re.DOTALL)
    
    for m in pattern.finditer(line):
        # Append literal text between the previous match and this one.
        literal = line[last_end:m.start()]
        if literal:
            # If there is an active group and the literal is not just whitespace, flush the group.
            if active_group is not None and not literal.isspace():
                output += f"<ls>{active_group['text']}</ls>"
                active_group = None
            output += literal
        
        full_tag = m.group(0)
        attrs = m.group("attrs")
        content = m.group("content").strip()
        
        # If the tag does not have an id attribute, preserve it exactly.
        if 'id="' not in attrs:
            if active_group is not None:
                output += f"<ls>{active_group['text']}</ls>"
                active_group = None
            output += full_tag
        else:
            # For tags with an id attribute, also try to capture the n attribute (if present)
            n_match = re.search(r'n="([^"]+)"', attrs)
            group_n = n_match.group(1) if n_match else None

            # Determine the rule: if content is only digits, commas, periods (and whitespace)
            if re.fullmatch(r"[0-9,.\s]+", content):
                # Rule 2: remove tag entirely; output just the inner text.
                group_type = "continuation"
                processed_piece = content
            else:
                # Rule 3: remove attributes; keep tag and inner text.
                group_type = "starter"
                processed_piece = content

            # Merging logic:
            if active_group is not None:
                # We are in the middle of a merged group.
                # If the current tag is a starter, then it always starts a new group.
                if group_type == "starter":
                    output += f"<ls>{active_group['text']}</ls>"
                    active_group = {"text": processed_piece, "group_n": group_n}
                else:  # continuation tag
                    # If the group identifier (n attribute) matches, merge.
                    if active_group["group_n"] == group_n:
                        active_group["text"] += " " + processed_piece
                    else:
                        # Different group: flush the active group and output the current processed piece.
                        output += f"<ls>{active_group['text']}</ls>"
                        active_group = None
                        output += processed_piece
            else:
                # No active group currently.
                if group_type == "starter":
                    active_group = {"text": processed_piece, "group_n": group_n}
                else:
                    # A continuation tag without a preceding starter: output plain text.
                    output += processed_piece
        
        last_end = m.end()
    
    # Append any literal text after the last match.
    literal = line[last_end:]
    if literal:
        if active_group is not None and not literal.isspace():
            output += f"<ls>{active_group['text']}</ls>"
            active_group = None
        output += literal
    else:
        if active_group is not None:
            output += f"<ls>{active_group['text']}</ls>"
            active_group = None
            
    return output

def main():
    if len(sys.argv) < 3:
        print("Usage: python reverse_script.py <transformed_file> <reversed_output_file>")
        sys.exit(1)
    
    transformed_file = sys.argv[1]
    reversed_output_file = sys.argv[2]
    
    with open(transformed_file, 'r', encoding='utf-8') as fin, open(reversed_output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            reversed_line = reverse_transform_ls_tags(line)
            fout.write(reversed_line)
    
    print("Reversal complete. Output saved to", reversed_output_file)

if __name__ == "__main__":
    main()
