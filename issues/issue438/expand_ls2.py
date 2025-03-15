import sys
import re
import csv

def load_book_list(tsv_file):
    book_list = []
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) == 2:
                book_list.append((row[0], int(row[1])))
    return book_list

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
        #print(f"Processing book: {book_name}")
        numbers = match.group(2).split()
        
        expected_length, labels = book_formats[book_name]
        occurrences = []
        first = True
        last_values.setdefault(book_name, [''] * expected_length)
        last_book_name = book_name  # Store last encountered book name
        
        for number in numbers:
            number_parts = number.rstrip('.').split(',')
            
            number_parts = (last_values[book_name][:expected_length - len(number_parts)] + number_parts)[-expected_length:]
            last_values[book_name] = number_parts
            number_cleaned = ','.join(filter(None, number_parts))  # Remove None values
            
            if first:
                occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{book_name} {number}</ls>')
                first = False
            else:
                occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{number}</ls>')
        
        return " ".join(occurrences)
    
    for book, _ in book_list:
        print(f"Handling book: {book}")
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
            
            number_cleaned = ','.join(filter(None, number_parts))  # Remove None values
            occurrences.append(f'<ls n="{last_book_name}" id="{number_cleaned}">{number}</ls>')
        
        return " ".join(occurrences)
    
    pattern_missing = re.compile(r"<ls>\s*([0-9,\.\s]+)\s*</ls>")
    data = pattern_missing.sub(fill_missing_values, data)
    
    return data

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <input_file> <book_name.tsv> <output_file>")
        return
    
    input_file = sys.argv[1]
    tsv_file = sys.argv[2]
    output_file = sys.argv[3]
    
    book_list = load_book_list(tsv_file)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()
    
    transformed_data = transform_ls_tags(data, book_list)
    
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(transformed_data)
    
    print("Transformation complete. Output saved to", output_file)

if __name__ == "__main__":
    main()
