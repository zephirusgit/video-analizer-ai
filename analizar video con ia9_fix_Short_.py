import os
import subprocess
from PIL import Image
from datetime import timedelta
import json
import requests
from typing import Dict
import PyPDF2

# Configuración de los directorios y archivos
video_path = "video.mp4"
frames_dir = "frames"
bitacora_path = "bitacora.json"
transcription_txt = "video.txt"
pdf_path = "mi_pdf.pdf"
ocr_output_pdf = "adocr.pdf"
ocr_txt_path = "ocrmy_pdf.txt"
final_summary_path = "resumen_final.txt"
sample_script_path = "sample.py"  # Ruta del script de MoonDream
ollama_url = "http://localhost:11434/api/generate"

# Crear directorio para los cuadros extraídos
os.makedirs(frames_dir, exist_ok=True)

def transcribir_audio(video_path):
    """Utiliza Whisper desde la línea de comandos para transcribir el audio."""
    subprocess.run([
        "whisper", video_path, "--task", "transcribe", "--output_format", "txt"
    ])
    with open(transcription_txt, "r", encoding="utf-8") as f:
        transcripcion = f.read().strip()
    return transcripcion

def extraer_cuadros(video_path, frames_dir, frame_interval=2):
    """Extrae cuadros del video usando ffmpeg cada 'frame_interval' segundos."""
    subprocess.run([
        "ffmpeg", 
        "-i", video_path, 
        "-vf", f"fps=1/{frame_interval}",  # Un cuadro cada 'frame_interval' segundos
        os.path.join(frames_dir, "frame_%04d.png")
    ])
    print("Cuadros extraídos.")

def analizar_cuadro_moondream(image_path: str, prompt="describe la imagen por favor? responde en español") -> Dict:
    """
    Analiza una imagen utilizando un modelo de LLM con un esquema detallado para describir escenas.
    
    Args:
        image_path (str): La ruta de la imagen que se analizará.
        prompt (str): Prompt base para solicitar la descripción de la imagen. Este se ampliará automáticamente.

    Returns:
        Dict: Un diccionario con la descripción detallada de la escena.
    """
    result = subprocess.run(
        ["python", sample_script_path, "--image", image_path, "--prompt", prompt],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error ejecutando MoonDream: {result.stderr}")
        return {"error": result.stderr.strip()}
    
    # Ejemplo de procesamiento extendido
    description = result.stdout.strip()
    analysis = {
        "image_path": image_path,
        "description": description,
        "metadata": {
            "analysis_tool": "MoonDream",
            "prompt_used": prompt
        }
    }
    return analysis

def generar_bitacora(frames_dir):
    """Genera una bitácora de eventos analizando los cuadros extraídos."""
    bitacora = []
    for frame_file in sorted(os.listdir(frames_dir)):
        frame_path = os.path.join(frames_dir, frame_file)
        print(f"Analizando cuadro: {frame_file}")
        moondream_result = analizar_cuadro_moondream(frame_path)
        evento = {
            "frame": frame_file,
            "moondream": moondream_result
        }
        bitacora.append(evento)
    with open(bitacora_path, "w", encoding="utf-8") as f:
        json.dump(bitacora, f, indent=4, ensure_ascii=False)
    return bitacora

def convert_images_to_pdf(image_folder, output_pdf):
    """Convierte imágenes a un archivo PDF."""
    image_list = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path).convert('RGB')
            image_list.append(image)
    if image_list:
        image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
        print(f"PDF generado correctamente en {output_pdf}")
    else:
        print("No se encontraron imágenes PNG en la carpeta.")

def aplicar_ocr_al_pdf(input_pdf, output_pdf):
    """Aplica OCR a un PDF usando ocrmypdf."""
    try:
        subprocess.run(
            ["ocrmypdf", "--skip-text", input_pdf, output_pdf],
            check=True
        )
        print(f"OCR aplicado correctamente. Archivo guardado en {output_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"Error al aplicar OCR: {e}")
        raise

def extract_text_from_pdf(pdf_file_path):
    """Extrae texto de un PDF y lo guarda en un archivo .txt."""
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join(page.extract_text() for page in reader.pages)
    return text

def procesar_pdf_con_ocr(input_pdf, ocr_output_pdf, ocr_txt_path):
    """Aplica OCR al PDF y extrae el texto resultante."""
    aplicar_ocr_al_pdf(input_pdf, ocr_output_pdf)
    texto_extraido = extract_text_from_pdf(ocr_output_pdf)
    with open(ocr_txt_path, 'w', encoding='utf-8') as f:
        f.write(texto_extraido)
    print(f"Texto extraído del PDF con OCR guardado en {ocr_txt_path}")
    return texto_extraido

def interact_with_ollama(prompt):
    """Interactúa con Ollama para obtener una respuesta."""
    payload = {"model": "llama3", "prompt": prompt}
    try:
        with requests.post(ollama_url, json=payload, stream=True) as response:
            response.raise_for_status()
            result = ""
            for line in response.iter_lines():
                if line:
                    json_data = json.loads(line.decode('utf-8'))
                    result += json_data.get("response", "")
            return result.strip()
    except requests.RequestException as e:
        print(f"Error al interactuar con Ollama: {e}")
        return ""

def generar_resumen_final(transcripcion, bitacora, ocr_texto):
    """Genera un resumen final basado en los datos parciales."""
    resumen_transcripcion = interact_with_ollama(
        f"Resumen del audio transcrito: {transcripcion}"
    )
    resumen_bitacora = interact_with_ollama(
        f"Describe lo que se ve en las imágenes basado en la bitácora: {json.dumps(bitacora, ensure_ascii=False)}"
    )
    resumen_ocr = interact_with_ollama(
        f"Resumen del texto extraído del PDF: {ocr_texto}"
    )
    resumen_final = interact_with_ollama(
        f"Basándote en estos tres resúmenes, describe de qué trata el video:\n"
        f"- Transcripción del audio: {resumen_transcripcion}\n"
        f"- Análisis de imágenes: {resumen_bitacora}\n"
        f"- Texto del OCR: {resumen_ocr}"
    )
    with open(final_summary_path, "w", encoding="utf-8") as f:
        f.write(f"Resumen de transcripción:\n{resumen_transcripcion}\n\n")
        f.write(f"Resumen de imágenes:\n{resumen_bitacora}\n\n")
        f.write(f"Resumen de texto OCR:\n{resumen_ocr}\n\n")
        f.write(f"Resumen final del video:\n{resumen_final}")
    print(f"Resumen final guardado en {final_summary_path}")

# --- FLUJO PRINCIPAL ---
if __name__ == "__main__":
    print("1. Transcribiendo audio con Whisper...")
    transcripcion = transcribir_audio(video_path)
    
    print("2. Extrayendo cuadros con FFmpeg...")
    extraer_cuadros(video_path, frames_dir, frame_interval=30)
   
    print("3. Generando bitácora de imágenes...")
    bitacora = generar_bitacora(frames_dir)
    
    print("4. Generando PDF de cuadros...")
    convert_images_to_pdf(frames_dir, pdf_path)
    
    print("5. Aplicando OCR y extrayendo texto del PDF...")
    ocr_texto = procesar_pdf_con_ocr(pdf_path, ocr_output_pdf, ocr_txt_path)
    
    print("6. Generando resumen final con Ollama...")
    generar_resumen_final(transcripcion, bitacora, ocr_texto)
