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

def transform_ls_tags(text, book_names):
    """
    Transform <ls> tags by splitting alphanumeric references.

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

        # Extract the reference part after the book name
        remaining_text = full_match[len(book_name):].strip()
        references = re.findall(r'(\d+,[ab],\d+)', remaining_text)
        print(book_name, references)

        # If no references are found, return the original tag
        if not references:
            return match.group(0)

        last_full_ref = None
        transformed_ls_tags = []

        for ref in references:
            parts = ref.split(',')

            if len(parts) == 3:
                last_full_ref = ref
            elif len(parts) == 2:
                if last_full_ref:
                    last_full_ref = f"{last_full_ref.split(',')[0]},{ref}"
                else:
                    return match.group(0)  # If missing reference, return original tag
            elif len(parts) == 1:
                if last_full_ref:
                    last_full_ref = f"{last_full_ref.rsplit(',', 1)[0]},{ref}"
                else:
                    return match.group(0)  # If missing reference, return original tag

            transformed_ls_tags.append(f'<ls n="{book_name}" id="{last_full_ref}">{last_full_ref}.</ls>')

        return f'<ls n="{book_name}" id="{references[0]}">{book_name} {references[0]}.</ls> ' + " ".join(transformed_ls_tags[1:])

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
