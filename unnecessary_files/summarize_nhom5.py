with open('scratch/nhom_5_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')

with open('scratch/nhom_5_summary.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total lines: {len(lines)}\n\n")
    out.write("=== HEADINGS AND KEY SECTIONS ===\n")
    for i, line in enumerate(lines):
        line_s = line.strip()
        if line_s.startswith('[Heading') or any(line_s.startswith(x) for x in ['CHƯƠNG', 'Chương', 'PHẦN', 'Phần', 'MỤC LỤC', '1.', '2.', '3.', '4.', '5.', '6.']):
            out.write(f"L{i+1}: {line_s}\n")

print("Summary written")
