import sys
import re

def determine_format(numbers):
    parts = [num.split(',') for num in numbers]
    max_length = max(len(part) for part in parts)
    
    if max_length == 4:
        return ["volume", "chapter", "section", "line"]
    elif max_length == 3:
        return ["chapter", "section", "line"]
    elif max_length == 2:
        return ["section", "line"]
    else:
        return ["line"]

def transform_ls_tags(data, book_list):
    book_formats = {}
    last_values = {}
    
    def replace_match(match):
        book_name = match.group(1)
        numbers = match.group(2).split()
        
        if book_name not in book_formats:
            book_formats[book_name] = determine_format(numbers)
        
        occurrences = []
        first = True
        last_values.setdefault(book_name, [None] * len(book_formats[book_name]))
        
        for number in numbers:
            number_parts = number.rstrip('.').split(',')
            expected_length = len(book_formats[book_name])
            
            number_parts = (last_values[book_name][:expected_length - len(number_parts)] + number_parts)[-expected_length:]
            last_values[book_name] = number_parts
            number_cleaned = ','.join(number_parts)
            
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
