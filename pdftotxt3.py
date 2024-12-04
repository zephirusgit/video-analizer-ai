import PyPDF2
import os

# Función para leer el contenido de un PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Función para guardar el contenido en un archivo .txt
def save_text_to_file(text, file_path):
    txt_file_path = file_path.replace('.pdf', '.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    return txt_file_path

# Función principal
def main(pdf_file_path):
    # Leer y extraer el contenido del PDF
    pdf_content = read_pdf(pdf_file_path)
    # Guardar el contenido en un archivo .txt
    txt_file_path = save_text_to_file(pdf_content, pdf_file_path)
    print(f"PDF content has been saved to {txt_file_path}")

if __name__ == "__main__":
    # Ruta al archivo PDF
    pdf_file_path = "adocr.pdf"
    try:
        main(pdf_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
