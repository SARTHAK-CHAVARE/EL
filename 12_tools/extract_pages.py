import pymupdf

doc = pymupdf.open(r"c:\Project\EL\030 EL Rubrics (1).pdf")
print(f"Number of pages: {len(doc)}")

for i, page in enumerate(doc):
    # Extract images from the page
    images = page.get_images()
    print(f"\nPage {i+1}: {len(images)} images found")
    
    # Get page as pixmap (render to image)
    pix = page.get_pixmap(dpi=300)
    output_path = f"c:\\Project\\EL\\page_{i+1}.png"
    pix.save(output_path)
    print(f"  Saved page image to {output_path}")
    
    # Try to get text blocks
    blocks = page.get_text("blocks")
    if blocks:
        for b in blocks:
            print(f"  Text block: {b[4][:100] if b[4].strip() else '(empty)'}...")

doc.close()
print("\nDone!")
