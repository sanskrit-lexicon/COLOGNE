import sys
import random
import xml.etree.ElementTree as ET

def process_xml(xml_file, x, output_md_file):
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Ensure root tag is 'pwg'
    if root.tag != "pwg":
        raise ValueError("Unexpected root tag. Expected 'pwg'.")
    
    # Collect all H1 entries
    h1_entries = root.findall(".//H1")
    
    # Collect ls elements with their corresponding H1 context
    ls_data = []
    for h1 in h1_entries:
        key1_elem = h1.find(".//h/key1")
        key1 = key1_elem.text.strip() if key1_elem is not None and key1_elem.text else ""
        
        L_elem = h1.find(".//tail/L")
        L = L_elem.text.strip() if L_elem is not None and L_elem.text else ""
        
        pc_elem = h1.find(".//tail/pc")
        pc = pc_elem.text.strip() if pc_elem is not None and pc_elem.text else ""
        
        ls_tags = [ls for ls in h1.findall(".//ls") if "id" in ls.attrib]
        
        for ls in ls_tags:
            n_attr = ls.attrib.get("n", "")
            ls_data.append((L, key1, pc, n_attr, ls.attrib["id"]))
    
    # Select X random ls entries
    selected_ls = random.sample(ls_data, min(x, len(ls_data)))
    
    # Generate Markdown content
    md_content = "| L | Key1 | n | ID | yes/no |\n"
    md_content += "|---|------|---|----|-------|\n"
    for L, key1, pc, n_attr, ls_id in selected_ls:
        md_content += f"| {L} | [{key1}](https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=PWG&page={pc}) | {n_attr} | {ls_id} |  |\n"
    
    # Save to an MD file
    with open(output_md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"Markdown file '{output_md_file}' generated successfully.")

if __name__ == "__main__":
    xml_file = sys.argv[1]
    x = int(sys.argv[2])  # Number of random ls tags
    output_md_file = sys.argv[3]
    process_xml(xml_file, x, output_md_file)
