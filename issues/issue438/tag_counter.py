import xml.etree.ElementTree as ET
import sys
import re
from collections import Counter

# List of whitelisted `n` attribute values
WHITELISTED_N_VALUES = {'HALL', 'WASSILJEW', 'VARARUCI', 'YAŚNA', 'HIOUEN-THSANG', 'CARAKA', 'VĀMANA', 'WIND. Sancara', 'COWELL', 'WILSON, Sel. Works', 'KṚṢISAṂGRAHA', 'Vie de HIOUEN-THSANG', 'ŚIKṢĀ', 'KĀTANTRA', 'KĀLACAKRA'}

def count_ls_tags(xml_file):
    """
    Parses an XML file and counts occurrences of <ls> tags based on their attributes.
    """
    with open(xml_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    tree = ET.ElementTree(ET.fromstring(content))
    root = tree.getroot()
    
    total_ls_tags = 0
    ls_with_n_and_id = 0
    ls_with_only_n = 0
    ls_with_only_n_comma = 0
    ls_with_only_n_period = 0
    ls_with_only_n_bracket = 0
    ls_with_only_n_whitelisted = 0
    ls_with_only_n_other = 0
    ls_without_attrs = 0
    ls_without_attrs_with_number = 0
    ls_without_attrs_no_number = 0
    book_name_counter = Counter()

    comma_pattern = re.compile(r',\s*$')
    period_pattern = re.compile(r'\.\s*$')
    bracket_pattern = re.compile(r'\)\s*$')
    number_pattern = re.compile(r'\d+')
    book_name_pattern = re.compile(r'([\w.\s-]+?)\s*\d')  # Captures book names before numbers

    for ls in root.findall('.//ls'):
        total_ls_tags += 1
        n_attr = 'n' in ls.attrib
        id_attr = 'id' in ls.attrib
        ls_text = (ls.text or "").strip()
        n_value = ls.attrib.get('n', "").strip()

        if n_attr and id_attr:
            ls_with_n_and_id += 1
        elif n_attr:
            ls_with_only_n += 1
            if n_value in WHITELISTED_N_VALUES:
                ls_with_only_n_whitelisted += 1
            elif comma_pattern.search(n_value):
                ls_with_only_n_comma += 1
            elif period_pattern.search(n_value):
                ls_with_only_n_period += 1
            elif bracket_pattern.search(n_value):
                ls_with_only_n_bracket += 1
            else:
                ls_with_only_n_other += 1
        elif not ls.attrib:
            ls_without_attrs += 1
            if number_pattern.search(ls_text):
                ls_without_attrs_with_number += 1
                match = book_name_pattern.search(ls_text)
                if match:
                    book_name_counter[match.group(1).strip()] += 1
            else:
                ls_without_attrs_no_number += 1

    def percentage(part, whole):
        return f"{(part / whole * 100):6.2f}%" if whole > 0 else "  0.00%"

    print("\nTag Count Statistics")
    print("=" * 55)
    print(f"{'Category':<45} {'Count':>6}  {'Percentage':>10}")
    print("-" * 55)
    print(f"{'Total <ls> tags':<45} {total_ls_tags:>6}  {percentage(total_ls_tags, total_ls_tags)}")
    print(f"{'<ls> tags with both n and id':<45} {ls_with_n_and_id:>6}  {percentage(ls_with_n_and_id, total_ls_tags)}")
    print(f"{'<ls> tags with only n':<45} {ls_with_only_n:>6}  {percentage(ls_with_only_n, total_ls_tags)}")
    print(f"{'  - n attribute ending with a comma':<45} {ls_with_only_n_comma:>6}  {percentage(ls_with_only_n_comma, total_ls_tags)}")
    print(f"{'  - n attribute ending with a period':<45} {ls_with_only_n_period:>6}  {percentage(ls_with_only_n_period, total_ls_tags)}")
    print(f"{'  - n attribute ending with a closing bracket':<45} {ls_with_only_n_bracket:>6}  {percentage(ls_with_only_n_bracket, total_ls_tags)}")
    print(f"{'  - Whitelisted values':<45} {ls_with_only_n_whitelisted:>6}  {percentage(ls_with_only_n_whitelisted, total_ls_tags)}")
    print(f"{'  - Other cases':<45} {ls_with_only_n_other:>6}  {percentage(ls_with_only_n_other, total_ls_tags)}")
    print(f"{'<ls> tags without any attributes':<45} {ls_without_attrs:>6}  {percentage(ls_without_attrs, total_ls_tags)}")
    print(f"{'  - Without attributes but with numbers':<45} {ls_without_attrs_with_number:>6}  {percentage(ls_without_attrs_with_number, total_ls_tags)}")
    print(f"{'  - Without attributes and no numbers':<45} {ls_without_attrs_no_number:>6}  {percentage(ls_without_attrs_no_number, total_ls_tags)}")
    print("=" * 55)

    print("\nMost Frequent Book Names in <ls> without attributes but with numbers:")
    print("-" * 55)
    for book, count in book_name_counter.most_common():
        print(f"{book}: {count} times")
    print("-" * 55)

    return {
        "total_ls_tags": total_ls_tags,
        "ls_with_n_and_id": ls_with_n_and_id,
        "ls_with_only_n": ls_with_only_n,
        "ls_with_only_n_comma": ls_with_only_n_comma,
        "ls_with_only_n_period": ls_with_only_n_period,
        "ls_with_only_n_bracket": ls_with_only_n_bracket,
        "ls_with_only_n_whitelisted": ls_with_only_n_whitelisted,
        "ls_with_only_n_other": ls_with_only_n_other,
        "ls_without_attrs": ls_without_attrs,
        "ls_without_attrs_with_number": ls_without_attrs_with_number,
        "ls_without_attrs_no_number": ls_without_attrs_no_number
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tag_counter.py <xml_file>")
        sys.exit(1)
    xml_file = sys.argv[1]
    try:
        count_ls_tags(xml_file)
    except ET.ParseError as e:
        print(f"Error: Failed to parse XML file. {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{xml_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)