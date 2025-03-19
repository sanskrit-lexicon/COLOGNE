"""
expand_ls4.py

This script reads an input file and a CSV file containing book names, then transforms occurrences of `<ls>` tags 
containing those book names and numerical references into an expanded format with `n` and `id` attributes.

Specifically, it transforms:
    `<ls>{book_name} ([0-9,.]+)</ls>`  
into:
    `<ls n="\1" id="\2">\1 \2</ls>`

where `{book_name}` is dynamically loaded from a CSV file.

Usage:
    python expand_ls4.py input.txt books.csv output.txt

Arguments:
    input.txt   - Path to the input file containing text with `<ls>` tags.
    books.csv   - Path to a CSV file where the first column contains book names.
    output.txt  - Path to the output file where transformed text will be saved.

Example:
    If the input file contains:
        "This is a reference <ls>AK. 12,34</ls> in the text."
    And books.csv contains:
        AK.
        TRIK.
    The output file will contain:
        "This is a reference <ls n="AK." id="12,34">AK. 12,34</ls> in the text."

Author: Dhaval
"""

import re
import sys
import csv

def load_book_names(csv_file):
    """
    Loads book names from the first column of a CSV file.

    Args:
        csv_file (str): Path to the CSV file containing book names.

    Returns:
        list: A list of book names.
    """
    book_names = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            book_names = [row[0].strip() for row in reader if row]
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    return book_names

def expand_ls_tags(text, book_names):
    """
    Expands <ls> tags containing book names and numerical references to include `n` and `id` attributes.

    Args:
        text (str): The input text containing <ls> tags.
        book_names (list of str): List of valid book names loaded from the CSV file.

    Returns:
        str: The transformed text with expanded <ls> tags.
    """
    # Create a regex pattern dynamically based on known book names
    book_pattern = r"(" + "|".join(map(re.escape, book_names)) + r")"
    pattern = rf"<ls>{book_pattern}\s*([0-9,.]+)</ls>"
    
    # Perform the transformation
    transformed_text = re.sub(pattern, r'<ls n="\1" id="\2">\1 \2</ls>', text)
    return transformed_text

def main():
    """
    Main function to read input file, load book names from CSV, transform the text, and write to output file.
    """
    if len(sys.argv) != 4:
        print("Usage: python expand_ls4.py input.txt books.csv output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    csv_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # Load book names from CSV
    book_names = load_book_names(csv_file)
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Transform the text
        transformed_text = expand_ls_tags(text, book_names)
        
        # Write to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transformed_text)
        
        print(f"Transformation complete. Output saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
