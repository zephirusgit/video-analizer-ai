import os
from PIL import Image

def convert_images_to_pdf(image_folder, output_pdf):
    image_list = []

    for filename in os.listdir(image_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path).convert('RGB')  # Convertir a RGB para compatibilidad con PDF
            image_list.append(image)

    if image_list:
        image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
        print(f"PDF generado correctamente en {output_pdf}")
    else:
        print("No se encontraron imágenes PNG en la carpeta.")

# Ejemplo de uso:
image_folder = "./frames"
output_pdf = "mi_pdf.pdf"
convert_images_to_pdf(image_folder, output_pdf)
