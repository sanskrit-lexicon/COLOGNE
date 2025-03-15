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
    are merged into a single <ls>…</ls> group while preserving proper spacing.
    """
    output = []
    last_end = 0
    active_group = None  # Stores {'text': "...", 'group_n': "..."}
    trailing_space = ""

    # Regex pattern to match any <ls ...>...</ls> (non-greedy)
    pattern = re.compile(r'(\s*)<ls(?P<attrs>[^>]*)>(?P<content>.*?)</ls>(\s*)', re.DOTALL)

    for m in pattern.finditer(line):
        leading_space = m.group(1)  # Space before <ls>
        full_tag = m.group(0)
        attrs = m.group("attrs")
        content = m.group("content").strip()
        trailing_space = m.group(4)  # Space after </ls>

        # Append literal text between the previous match and this one.
        literal = line[last_end:m.start()]
        if literal:
            if active_group:
                output.append(f"<ls>{active_group['text']}</ls>")
                active_group = None
            output.append(literal)

        # If the tag does not have an id attribute, preserve it exactly.
        if 'id="' not in attrs:
            if active_group:
                output.append(f"<ls>{active_group['text']}</ls>")
                active_group = None
            output.append(leading_space + full_tag + trailing_space)
        else:
            # Extract n attribute if present
            n_match = re.search(r'n="([^"]+)"', attrs)
            group_n = n_match.group(1) if n_match else None

            # Determine rule: if content is only digits, commas, periods (and whitespace)
            if re.fullmatch(r"[0-9,.\s]+", content):
                group_type = "continuation"
                processed_piece = content
            else:
                group_type = "starter"
                processed_piece = content

            # Merging logic:
            if active_group:
                if group_type == "starter":
                    output.append(f"<ls>{active_group['text']}</ls>")
                    active_group = {"text": processed_piece, "group_n": group_n}
                else:
                    if active_group["group_n"] == group_n:
                        active_group["text"] += " " + processed_piece
                    else:
                        output.append(f"<ls>{active_group['text']}</ls>")
                        active_group = {"text": processed_piece, "group_n": group_n}
            else:
                if group_type == "starter":
                    active_group = {"text": processed_piece, "group_n": group_n}
                else:
                    output.append(leading_space + processed_piece + trailing_space)

        last_end = m.end()

    # Append any remaining literal text after the last match
    literal = line[last_end:]
    if literal:
        if active_group:
            output.append(f"<ls>{active_group['text']}</ls>")
            active_group = None
        output.append(literal)
    elif active_group:
        output.append(f"<ls>{active_group['text']}</ls>")
        active_group = None

    return "".join(output)

def main():
    if len(sys.argv) < 3:
        print("Usage: python reverse_script.py <transformed_file> <reversed_output_file>")
        sys.exit(1)
    
    transformed_file = sys.argv[1]
    reversed_output_file = sys.argv[2]
    
    with open(transformed_file, 'r', encoding='utf-8') as fin, open(reversed_output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            reversed_line = reverse_transform_ls_tags(line)
            fout.write(reversed_line + "\n")
    
    print("Reversal complete. Output saved to", reversed_output_file)

if __name__ == "__main__":
    main()
