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
    """
    def process_match(match):
        tag_content = match.group("content").strip()
        attrs = match.group("attrs") or ""  # Handle cases where attrs might be None

        # If the tag does not have an id attribute, preserve it as it is
        if 'id="' not in attrs:
            return f"<ls{attrs}>{tag_content}</ls>"

        # If content is ONLY numbers, commas, or periods, remove the <ls> tag completely
        if re.fullmatch(r"[0-9,.\s]+", tag_content):
            return tag_content

        # Otherwise, keep <ls> but remove attributes
        return f"<ls>{tag_content}</ls>"

    # Updated regex to correctly capture <ls> tags and their attributes
    pattern = re.compile(r'<ls(?P<attrs>\s[^>]*)?>(?P<content>.*?)</ls>', re.DOTALL)
    return pattern.sub(process_match, line)

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
