import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import sys
import os

# Path to Tesseract executable (may need to be specified like this on Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_with_ocr(image_path, lang="fas+ara+eng"):
    """
    Receives the path of an image file and extracts text using Tesseract.
    Adjust 'lang' to match the desired languages (Farsi, Arabic, English).
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        print(f"Error during OCR extraction for {image_path}: {e}")
        return ""

def create_output_folder(pdf_path):
    """
    Creates an output folder based on the PDF file name.
    The folder will be created in the same directory as the PDF.
    """
    try:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = os.path.join(os.path.dirname(__file__), base_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        return output_folder
    except Exception as e:
        print(f"Error creating output folder: {e}")
        raise

def process_pdf(pdf_path, ocr_lang="fas+ara+eng", zoom_factor=2):
    """
    pdf_path: Path to the PDF file.
    ocr_lang: Languages used for OCR (combined, e.g., 'fas+ara+eng').
    zoom_factor: Zoom factor for rendering the page (to improve OCR quality).
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return
    
    output_folder = create_output_folder(pdf_path)
    
    for page_number in range(len(doc)):
        try:
            page = doc.load_page(page_number)
        except Exception as e:
            print(f"Error loading page {page_number + 1}: {e}")
            continue
        
        # Attempt to extract text using the normal method
        try:
            extracted_text = page.get_text("text")
        except Exception as e:
            print(f"Error extracting text from page {page_number + 1}: {e}")
            extracted_text = ""
        
        # Output text filename and output image filename
        text_filename = os.path.join(output_folder, f"page_{page_number + 1}.txt")
        image_filename = os.path.join(output_folder, f"page_{page_number + 1}.png")
        
        # Render the page as an image (both for saving the image and for OCR)
        try:
            mat = fitz.Matrix(zoom_factor, zoom_factor)
            pix = page.get_pixmap(matrix=mat)
            pix.save(image_filename)  # Save the page image as PNG
            print(f"Page {page_number + 1} image saved in file '{image_filename}'.")
        except Exception as e:
            print(f"Error rendering or saving image for page {page_number + 1}: {e}")
            continue
        
        # If the normal text extraction returns too little or empty text, use OCR
        if len(extracted_text.strip()) < 30:
            print(f"Page {page_number + 1}: Text not found or too little. Using OCR...")
            extracted_text = extract_text_with_ocr(image_filename, lang=ocr_lang)
        
        # Save the final text to a .txt file
        try:
            with open(text_filename, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)
            print(f"Page {page_number + 1} text saved in file '{text_filename}'.")
        except Exception as e:
            print(f"Error saving text for page {page_number + 1}: {e}")
    
    try:
        doc.close()
    except Exception as e:
        print(f"Error closing PDF document: {e}")

def check_and_process_pdf(pdf_path):
    """
    Checks if the folder and PDF file exist, then processes the PDF.
    """
    folder_path = os.path.dirname(pdf_path)
    
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    if not os.path.exists(pdf_path):
        print(f"The file '{pdf_path}' does not exist.")
        return
    
    process_pdf(pdf_path)

if __name__ == "__main__":
    ocr_lang = "fas+ara+eng"
    pdf_path = r"D:\workspace\test_enviroment\convert_pdf_to_image\pdfs\c.pdf"
    
    try:
        check_and_process_pdf(pdf_path)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
