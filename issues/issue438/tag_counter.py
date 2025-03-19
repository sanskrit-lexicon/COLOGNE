import xml.etree.ElementTree as ET
import sys
import re


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
    ls_without_attrs = 0
    ls_without_attrs_with_number = 0  # No attributes, but contains a numerical entry
    ls_without_attrs_no_number = 0   # No attributes, and no numerical entry

    # Regular expression to detect numerical values inside <ls> tag text
    number_pattern = re.compile(r'\d+')

    # Iterate over all <ls> tags
    for ls in root.findall('.//ls'):
        total_ls_tags += 1
        n_attr = 'n' in ls.attrib
        id_attr = 'id' in ls.attrib

        if n_attr and id_attr:
            ls_with_n_and_id += 1
        elif n_attr:
            ls_with_only_n += 1
        elif not ls.attrib:  # No attributes present
            ls_without_attrs += 1
            ls_text = (ls.text or "").strip()  # Get text inside <ls>, handle None case
            
            if number_pattern.search(ls_text):  # If text contains a number
                ls_without_attrs_with_number += 1
            else:
                ls_without_attrs_no_number += 1

    # Function to calculate percentage
    def percentage(part, whole):
        return f"{(part / whole * 100):6.2f}%" if whole > 0 else "  0.00%"

    # Print results in tabular format with proper alignment
    print("\nTag Count Statistics")
    print("=" * 50)
    print(f"{'Category':<42} {'Count':>6}  {'Percentage':>10}")
    print("-" * 50)
    print(f"{'Total <ls> tags':<42} {total_ls_tags:>6}  {percentage(total_ls_tags, total_ls_tags)}")
    print(f"{'<ls> tags with both n and id':<42} {ls_with_n_and_id:>6}  {percentage(ls_with_n_and_id, total_ls_tags)}")
    print(f"{'<ls> tags with only n':<42} {ls_with_only_n:>6}  {percentage(ls_with_only_n, total_ls_tags)}")
    print(f"{'<ls> tags without any attributes':<42} {ls_without_attrs:>6}  {percentage(ls_without_attrs, total_ls_tags)}")
    print(f"{'  - Without attributes but with numbers':<42} {ls_without_attrs_with_number:>6}  {percentage(ls_without_attrs_with_number, total_ls_tags)}")
    print(f"{'  - Without attributes and no numbers':<42} {ls_without_attrs_no_number:>6}  {percentage(ls_without_attrs_no_number, total_ls_tags)}")
    print("=" * 50)

    return {
        "total_ls_tags": total_ls_tags,
        "ls_with_n_and_id": ls_with_n_and_id,
        "ls_with_only_n": ls_with_only_n,
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
