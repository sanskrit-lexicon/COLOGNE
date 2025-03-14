import sys
import re

def find_ls_occurrences(data, book_list):
    occurrences = []
    for book in book_list:
        pattern = re.compile(fr"<ls>\s*({re.escape(book)})\s*([0-9,\.\s]+)\s*</ls>")
        matches = pattern.findall(data)
        for book_name, numbers in matches:
            number_list = numbers.split()
            first = True
            for number in number_list:
                number_cleaned = number.rstrip('.')
                if first:
                    occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{book_name} {number}</ls>')
                    first = False
                else:
                    occurrences.append(f'<ls n="{book_name}" id="{number_cleaned}">{number}</ls>')
    return occurrences

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        return
    
    input_file = sys.argv[1]
    book_list = ['H. an.', 'TRIK.', 'H.', 'AK.']
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()
    
    occurrences = find_ls_occurrences(data, book_list)
    for ls_tag in occurrences:
        print(ls_tag)

if __name__ == "__main__":
    main()
