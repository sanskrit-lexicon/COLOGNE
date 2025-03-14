import sys
import re

def transform_ls_tags(data, book_list):
    def replace_match(match):
        book_name = match.group(1)
        numbers = match.group(2).split()
        occurrences = []
        first = True
        for number in numbers:
            number_cleaned = number.rstrip('.')
            if first:
                occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{book_name} {number}</ls>')
                first = False
            else:
                occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{number}</ls>')
        return " ".join(occurrences)
    
    for book in book_list:
        pattern = re.compile(fr"<ls>\s*({re.escape(book)})\s*([0-9,\.\s]+)\s*</ls>")
        data = pattern.sub(replace_match, data)
    
    return data

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file>")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    book_list = ['H. an.', 'TRIK.', 'H.', 'AK.']
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()
    
    transformed_data = transform_ls_tags(data, book_list)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed_data)
    
    print("Transformation complete. Output saved to", output_file)

if __name__ == "__main__":
    main()
