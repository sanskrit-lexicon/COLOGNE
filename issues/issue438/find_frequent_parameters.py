import re
import sys
from collections import defaultdict

def parse_input(file_path):
    books = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith("*") and not line.startswith("**"):
                parts = line.split("\t")
                if len(parts) >= 2:
                    book_id = parts[1]
                    total_count = int(parts[0][1:].strip())
                    books[book_id] = {"total": total_count, "params": defaultdict(int)}
            elif line.startswith("**"):
                match = re.match(r"\*\* !?\((\d+)\) (.+) with (\d+|OTHER) numeric parameters", line)
                if match:
                    count = int(match.group(1))
                    book_id = match.group(2)
                    param = match.group(3)
                    
                    if param.isdigit():
                        param = int(param)  # Convert numeric parameters to integers
                    
                    if book_id in books:
                        books[book_id]["params"][param] += count
    
    return books

def find_most_frequent_parameter(books):
    results = []
    
    for book, details in books.items():
        total_count = details["total"]
        params = details["params"]
        
        valid_params = {k: v for k, v in params.items() if k != "OTHER" and k != 0 and v > 0.4 * total_count}
        
        if valid_params:
            most_frequent_param = max(valid_params, key=valid_params.get)
            most_frequent_param_count = valid_params[most_frequent_param]
            results.append((book, most_frequent_param, total_count, most_frequent_param_count))
        else:
            results.append((book, "NULL", total_count, 0))
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    books = parse_input(input_file)
    results = find_most_frequent_parameter(books)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()