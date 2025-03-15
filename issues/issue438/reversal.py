import re
import sys

def reverse_transform_ls_tags(line):
    """
    Reverse transforms a line according to the rules:
    
    1. If an <ls> tag does NOT have an id attribute, it is preserved exactly.
    2. If an <ls> tag has an id attribute and its inner text is only digits, commas, periods (and whitespace),
       then remove the <ls> tag entirely and output just the inner text.
    3. If an <ls> tag has an id attribute and its inner text contains other characters,
       then remove all attributes but keep the <ls> tag.
    4. If multiple <ls> tags originated from a single tag, merge them back into one.
    """

    def process_match(match):
        tag_content = match.group("content").strip()
        attrs = match.group("attrs") or ""

        # If no id attribute is present, preserve the tag as is
        if 'id="' not in attrs:
            return f"<ls{attrs}>{tag_content}</ls>"

        # If content is ONLY numbers, commas, or periods, remove the <ls> tag entirely
        if re.fullmatch(r"[0-9,.\s]+", tag_content):
            return tag_content

        # Otherwise, keep <ls> but remove attributes
        return f"<ls>{tag_content}</ls>"

    # Step 1: Remove attributes where needed
    pattern = re.compile(r'<ls(?P<attrs>\s[^>]*)?>(?P<content>.*?)</ls>', re.DOTALL)
    line = pattern.sub(process_match, line)

    # Step 2: Merge number fragments back into a single <ls> tag, ensuring only standalone numbers are merged
    line = re.sub(r'(<ls>([^<]+?)</ls>)\s+(\d+(?:,\d+|\.\d+)*\.?)(?!\w)', r'<ls>\2 \3</ls>', line)

    while re.search(r'(<ls>([^<]+?)</ls>)\s+(\d+(?:,\d+|\.\d+)*\.?)(?!\w)', line):
        line = re.sub(r'(<ls>([^<]+?)</ls>)\s+(\d+(?:,\d+|\.\d+)*\.?)(?!\w)', r'<ls>\2 \3</ls>', line)

    # Step 3: Correct handling of commas that succeed letters and precede numbers, but only within <ls> tags
    def fix_commas_within_ls(match):
        inner_text = match.group(1)
        fixed_text = re.sub(r'([a-zA-Z])\s*,\s*([0-9])', r'\1,\2', inner_text)
        return f"<ls>{fixed_text}</ls>"
    
    line = re.sub(r'<ls>(.*?)</ls>', fix_commas_within_ls, line)

    return line

def main():
    if len(sys.argv) < 3:
        print("Usage: python reverse_script.py <transformed_file> <reversed_output_file>")
        sys.exit(1)
    
    transformed_file = sys.argv[1]
    reversed_output_file = sys.argv[2]
    
    with open(transformed_file, 'r', encoding='utf-8') as fin, open(reversed_output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            reversed_line = reverse_transform_ls_tags(line)
            fout.write(reversed_line)  # No extra newline added
    
    print("Reversal complete. Output saved to", reversed_output_file)

if __name__ == "__main__":
    main()
