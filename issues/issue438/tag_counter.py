import xml.etree.ElementTree as ET
import sys
import re


# List of whitelisted `n` attribute values
WHITELISTED_N_VALUES = {'HALL', 'WASSILJEW', 'VARARUCI', 'YAŚNA', 'HIOUEN-THSANG', 'CARAKA', 'VĀMANA'}

def count_ls_tags(xml_file):
    """
    Parses an XML file and counts occurrences of <ls> tags based on their attributes.

    :param xml_file: Path to the XML file to be processed.
    :return: Dictionary containing statistics on <ls> tag counts.
    """
    
    # Read the file with UTF-8 encoding to avoid encoding issues
    with open(xml_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Parse the XML content
    tree = ET.ElementTree(ET.fromstring(content))
    root = tree.getroot()
    
    # Initialize counters
    total_ls_tags = 0
    ls_with_n_and_id = 0
    ls_with_only_n = 0
    ls_with_only_n_comma = 0  # 'n' attribute ends with a comma
    ls_with_only_n_period = 0  # 'n' attribute ends with a period
    ls_with_only_n_bracket = 0  # 'n' attribute ends with a closing bracket
    ls_with_only_n_whitelisted = 0  # 'n' attribute is in the whitelist
    ls_with_only_n_other = 0  # 'n' attribute ends with other characters
    ls_without_attrs = 0
    ls_without_attrs_with_number = 0  # No attributes, but contains a numerical entry
    ls_without_attrs_no_number = 0   # No attributes, and no numerical entry

    # List to store 'Other cases' for later printing
    ls_with_only_n_other_list = []

    # Regular expressions to detect endings in `n` attribute
    comma_pattern = re.compile(r',\s*$')
    period_pattern = re.compile(r'\.\s*$')
    bracket_pattern = re.compile(r'\)\s*$')  # Matches closing bracket `)`
    number_pattern = re.compile(r'\d+')  # Detects numerical values

    # Iterate over all <ls> tags
    for ls in root.findall('.//ls'):
        total_ls_tags += 1
        n_attr = 'n' in ls.attrib
        id_attr = 'id' in ls.attrib
        ls_text = (ls.text or "").strip()  # Get text inside <ls>, handle None case
        n_value = ls.attrib.get('n', "").strip()  # Get the 'n' attribute value safely

        if n_attr and id_attr:
            ls_with_n_and_id += 1
        elif n_attr:
            ls_with_only_n += 1

            # Categorize based on the `n` attribute's ending character
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
                ls_with_only_n_other_list.append(ET.tostring(ls, encoding='unicode').strip())

        elif not ls.attrib:  # No attributes present
            ls_without_attrs += 1
            if number_pattern.search(ls_text):  # If text contains a number
                ls_without_attrs_with_number += 1
            else:
                ls_without_attrs_no_number += 1

    # Function to calculate percentage
    def percentage(part, whole):
        return f"{(part / whole * 100):6.2f}%" if whole > 0 else "  0.00%"

    # Print results in tabular format with proper alignment
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

    # Print 'Other cases' from 'ls_with_only_n'
    print("\n<ls> tags with only 'n' attribute (Other cases):")
    print("-" * 55)
    for tag in ls_with_only_n_other_list:
        print(tag)
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
    """
    Usage:
    ------
    Run this script from the command line by providing the XML file as an argument:

        python tag_counter.py example.xml

    Ensure the XML file is valid and properly formatted.
    """
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
