import zipfile
import xml.etree.ElementTree as ET
import os

W_NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def extract_docx_structure(docx_path, out_txt_path):
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    
    with open(out_txt_path, 'w', encoding='utf-8') as f:
        # iterate body elements: p (paragraph) and tbl (table)
        body = tree.find('.//w:body', W_NS)
        if body is None:
            f.write("No body found\n")
            return
            
        for elem in body:
            tag = elem.tag.split('}')[-1]
            if tag == 'p':
                # check style
                pStyle = elem.find('.//w:pStyle', W_NS)
                style_val = pStyle.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '') if pStyle is not None else ''
                texts = [node.text for node in elem.iterfind('.//w:t', W_NS) if node.text]
                p_text = ''.join(texts).strip()
                if p_text:
                    if style_val:
                        f.write(f"[{style_val}] {p_text}\n")
                    else:
                        f.write(f"{p_text}\n")
            elif tag == 'tbl':
                f.write("\n--- [TABLE START] ---\n")
                for row in elem.iterfind('.//w:tr', W_NS):
                    row_cells = []
                    for cell in row.iterfind('.//w:tc', W_NS):
                        cell_texts = [node.text for node in cell.iterfind('.//w:t', W_NS) if node.text]
                        row_cells.append(' '.join(''.join(cell_texts).split()))
                    f.write(" | ".join(row_cells) + "\n")
                f.write("--- [TABLE END] ---\n\n")

os.makedirs('scratch', exist_ok=True)
extract_docx_structure('Báo_cáo_Nhóm_5_Testing.docx', 'scratch/nhom_5_extracted.txt')
extract_docx_structure('Báo_cáo_Nhóm_9_Testing.docx', 'scratch/nhom_9_extracted.txt')
print("Extracted successfully!")
