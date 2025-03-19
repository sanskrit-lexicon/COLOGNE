import re
import sys

def transform_ls_tags(input_file: str, output_file: str) -> None:
    """
    Transforms <ls> tags in a text file.

    This function reads an input file, finds occurrences of the pattern:
        <ls n="VALUE">NUMBER</ls>
    and converts them to:
        <ls n="VALUE" id="NUMBER">NUMBER</ls>
    
    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file where transformed text is stored.
    """
    # Regular expression pattern to match <ls> tags
    pattern = re.compile(r'<ls n="([^"]+)">([0-9,.]+)</ls>')
    
    # Read the input file content
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()
    
    # Perform the transformation using regex substitution
    transformed_content = pattern.sub(r'<ls n="\1" id="\2">\2</ls>', content)
    
    # Write the transformed content to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(transformed_content)

if __name__ == "__main__":
    """
    Entry point for the script.
    
    This script expects two command-line arguments:
    1. Path to the input file.
    2. Path to the output file.
    
    Usage::
        python expand_ls3.py input.txt output.txt
    """
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python expand_ls3.py input.txt output.txt")
        sys.exit(1)
    
    # Extract input and output file paths from command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Call the function to perform transformation
    transform_ls_tags(input_file, output_file)
