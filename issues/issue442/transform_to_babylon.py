import sys
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_headword = False
        self.in_definition = False
        self.headword = ""
        self.definition = ""
        self.entries = []
        self.definition_nest = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div" and "class" in attrs_dict:
            if attrs_dict["class"] == "headword":
                self.in_headword = True
            elif attrs_dict["class"] == "definition":
                self.in_definition = True
                self.definition_nest = 1
        
        if self.in_definition:
            attr_str = " ".join(f'{k}="{v}"' for k, v in attrs)
            self.definition += f"<{tag} {attr_str}>"
            if tag == "div":
                self.definition_nest += 1
        
    def handle_endtag(self, tag):
        if self.in_definition:
            self.definition += f"</{tag}>"
            if tag == "div":
                self.definition_nest -= 1
                if self.definition_nest == 0:
                    self.in_definition = False
                    if self.headword and self.definition:
                        self.entries.append((self.headword.strip(), self.definition.strip()))
                        self.headword = ""
                        self.definition = ""
        
        if tag == "div" and self.in_headword:
            self.in_headword = False
    
    def handle_data(self, data):
        if self.in_headword:
            self.headword += data.strip()
        elif self.in_definition:
            self.definition += data.replace("\n", "<br/>")

if len(sys.argv) < 3:
    print("Usage: python script.py input.html output.txt")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

parser = MyHTMLParser()
parser.feed(content)

with open(output_file, "w", encoding="utf-8") as file:
    file.write('\n#stripmethod=keep\n#sametypesequence=h\n#bookname=PWG\n\n')
    for headword, definition in parser.entries:
        definition = definition.replace('<br/>                    ', '')
        definition = definition.replace('<br/>                ', '')
        file.write(f"{headword}\n")
        #file.write("<style> body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; } .entry { margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px; box-shadow: 2px 2px 5px gray; } .headword { font-size: 24px; font-weight: bold; color: #333; } .alt-spelling { font-size: 18px; color: #555; } .metadata { font-size: 14px; color: #777; margin-top: 5px; } .definition { margin-left: 20px; font-size: 16px; } .sanskrit { font-family: 'Devanagari', serif; color: darkred; display: inline; } .citation { font-family: monospace; color: #0066cc; display: inline; margin-left: 5px; } .source { font-size: 14px; color: #777; } .indent-1 { margin-left: 20px; } .indent-2 { margin-left: 40px; } .indent-4 { margin-left: 80px; display: inline-block; } .ls-reference { font-family: 'Times New Roman', serif; color: lightgray; display: inline; margin-left: 5px; } </style> ")
        file.write(f"{definition}\n\n")

print(f"Processed HTML saved to {output_file}")
