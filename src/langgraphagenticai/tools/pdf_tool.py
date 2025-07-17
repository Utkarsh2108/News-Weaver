# src/langgraphagenticai/tools/pdf_tool.py

from markdown_pdf import MarkdownPdf, Section # ADDED: Import the Section class
import os

def convert_md_to_pdf(md_file_path: str) -> str:
    """Converts a markdown file to a PDF and returns the new PDF file path."""
    pdf_file_path = md_file_path.replace(".md", ".pdf")
    
    pdf = MarkdownPdf(toc_level=0)
    
    pdf.meta['title'] = os.path.basename(md_file_path)
    with open(md_file_path, 'r', encoding='utf-8') as f:
        # CHANGED: Wrap the markdown content in a Section object
        pdf.add_section(Section(f.read())) 
        
    pdf.save(pdf_file_path)
    return pdf_file_path