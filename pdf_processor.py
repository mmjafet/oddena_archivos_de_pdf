import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def extract_name(text):
    for line in text.split('\n'):
        if "ACREDITACIÓN DE OBSERVADOR(A) ELECTORAL" in line:
            parts = line.split("a (la/el)")
            if len(parts) > 1:
                return parts[1].strip().split(",")[0].strip()
    return "UNKNOWN"

def process_pdf(input_pdf_path, output_pdf_path):
    # Cargar PDF
    reader = PdfReader(input_pdf_path)
    names_and_pages = []

    # Extraer nombres por página
    with pdfplumber.open(input_pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            name = extract_name(text)
            names_and_pages.append((name, i))

    # Ordenar por nombre
    names_and_pages.sort(key=lambda x: x[0].lower())

    # Crear nuevo PDF ordenado
    writer = PdfWriter()
    for name, page_num in names_and_pages:
        writer.add_page(reader.pages[page_num])

    # Guardar resultado
    with open(output_pdf_path, "wb") as f:
        writer.write(f)
    
    return True