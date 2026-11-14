import fitz

doc = fitz.open(r"c:\Project\EL\030 EL Rubrics (1).pdf")
with open(r"c:\Project\EL\rubric_text.txt", "w", encoding="utf-8") as f:
    for i, page in enumerate(doc):
        f.write(f"=== PAGE {i+1} ===\n")
        f.write(page.get_text())
        f.write("\n\n")
doc.close()
print("Done - text saved to rubric_text.txt")
