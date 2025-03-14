import sys
import re

def find_ls_occurrences(data, book_list):
    occurrences = []
    for book in book_list:
        pattern = re.compile(fr"<ls>\s*({re.escape(book)})\s*([0-9,\.\s]+)\s*</ls>")
        matches = pattern.findall(data)
        occurrences.extend(matches)
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
    for book, numbers in occurrences:
        print(f"Found: <ls>{book} {numbers}</ls>")

if __name__ == "__main__":
    main()
