import sys
import re

def transform_ls_tags(data, book_list):
    book_formats = {
        book: (num_params, ['volume', 'chapter', 'section', 'line'][-num_params:])
        for book, num_params in book_list
    }
    last_values = {}
    last_book_name = None
    
    def replace_match(match):
        nonlocal last_book_name
        book_name = match.group(1)
        numbers = match.group(2).split()
        
        expected_length, labels = book_formats[book_name]
        occurrences = []
        first = True
        last_values.setdefault(book_name, [None] * expected_length)
        last_book_name = book_name  # Store last encountered book name
        
        for number in numbers:
            number_parts = number.rstrip('.').split(',')
            
            number_parts = (last_values[book_name][:expected_length - len(number_parts)] + number_parts)[-expected_length:]
            last_values[book_name] = number_parts
            number_cleaned = ','.join(number_parts)
            
            if first:
                occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{book_name} {number}</ls>')
                first = False
            else:
                occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{number}</ls>')
        
        return " ".join(occurrences)
    
    for book, _ in book_list:
        pattern = re.compile(fr"<ls>\s*({re.escape(book)})\s*([0-9,\.\s]+)\s*</ls>")
        data = pattern.sub(replace_match, data)
    
    def fill_missing_values(match):
        nonlocal last_book_name
        numbers = match.group(1).split()
        occurrences = []
        
        if last_book_name is None:
            return match.group(0)  # If no book encountered yet, return as is
        
        expected_length, labels = book_formats.get(last_book_name, (1, ['line']))
        
        for number in numbers:
            number_parts = number.rstrip('.').split(',')
            
            if len(number_parts) < expected_length:
                number_parts = (last_values[last_book_name][:expected_length - len(number_parts)] + number_parts)[-expected_length:]
                last_values[last_book_name] = number_parts
            
            number_cleaned = ','.join(number_parts)
            occurrences.append(f'<ls n="{last_book_name}" id="{number_cleaned}">{number}</ls>')
        
        return " ".join(occurrences)
    
    pattern_missing = re.compile(r"<ls>\s*([0-9,\.\s]+)\s*</ls>")
    data = pattern_missing.sub(fill_missing_values, data)
    
    return data

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file>")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    book_list = [('H. an.', 2), ('TRIK.', 3), ('H.', 1), ('AK.', 4)]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()
    
    transformed_data = transform_ls_tags(data, book_list)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed_data)
    
    print("Transformation complete. Output saved to", output_file)

if __name__ == "__main__":
    main()
