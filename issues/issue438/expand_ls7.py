import re
import sys
import csv

def load_book_names(book_file):
    """
    Load book names from a CSV file.
    :param book_file: Path to the CSV file containing book names.
    :return: A set of book names.
    """
    book_names = set()
    try:
        with open(book_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    book_names.add(row[0].strip())
    except FileNotFoundError:
        print(f"Warning: Book file '{book_file}' not found. Continuing without book names.")
    return book_names

def roman_to_int(roman):
    """
    Convert a Roman numeral to an integer.
    :param roman: Roman numeral as a string.
    :return: Integer representation.
    """
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    value, prev = 0, 0
    for char in reversed(roman):
        current = roman_numerals.get(char, 0)
        if current < prev:
            value -= current
        else:
            value += current
        prev = current
    return value

def transform_ls_tags(text, book_names):
    """
    Transform <ls> tags by handling Roman numerals in references.
    :param text: Input text containing <ls> tags.
    :param book_names: A set of known book names.
    :return: Transformed text.
    """
    def split_ls_match(match):
        """
        Process a single <ls> tag match and split references correctly.
        :param match: A regex match object.
        :return: Transformed <ls> tags or original tag if transformation is not possible.
        """
        full_match = match.group(1).strip()

        # Identify the book name
        book_name = None
        for name in sorted(book_names, key=len, reverse=True):
            if full_match.startswith(name):
                book_name = name
                break

        # If no book name is found, return the original tag
        if not book_name:
            return match.group(0)

        # Extract the remaining text after the book name
        remaining_text = full_match[len(book_name):].strip()

        # Match a Roman numeral followed by a comma and a number
        ref_match = re.match(r'([IVXLCDM]+),(\d+)', remaining_text)
        if not ref_match:
            return match.group(0)

        roman_part, numeric_part = ref_match.groups()
        numeric_id = f"{roman_to_int(roman_part)},{numeric_part}"

        return f'<ls n="{book_name}" id="{numeric_id}">{full_match}</ls>'

    # Apply transformation to all <ls> tags
    return re.sub(r'<ls>(.*?)</ls>', split_ls_match, text)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <book_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    book_file = sys.argv[2]
    output_file = sys.argv[3]

    # Load book names
    book_names_set = load_book_names(book_file)

    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    # Transform the text
    transformed_text = transform_ls_tags(input_text, book_names_set)

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed_text)

    print("Transformation complete. Output saved to", output_file)
