import os
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader

def convert_images_to_pdf(image_folder, output_pdf):
    pdf_writer = PdfWriter()

    for filename in os.listdir(image_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)  # Remove the extra space and number '1'
            pdf_page = pdf_writer.add_page()
            pdf_page.merge_image(image)

    with open(output_pdf, 'wb') as f:
        pdf_writer.write(f)

# Example of use:
image_folder = "./frames"
output_pdf = "mi_pdf.pdf"
convert_images_to_pdf(image_folder, output_pdf)