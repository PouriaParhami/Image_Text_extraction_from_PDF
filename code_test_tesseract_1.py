"""
Module: pdf_to_text_and_image.py

This module processes a given PDF file by extracting text and saving each page as an image.
For each page in the PDF, it first attempts to extract text using PyMuPDF. If the extracted text
is insufficient (less than 30 characters), it then uses Tesseract OCR via pytesseract to extract
text from the page image. The page image is also saved as a PNG file.
All extracted texts and images are saved in an output folder named after the PDF file (without extension).

Dependencies:
- PyMuPDF (install via 'pip install pymupdf')
- pytesseract (install via 'pip install pytesseract')
- Pillow (install via 'pip install Pillow')
- Tesseract OCR must be installed on the system and its executable path should be set appropriately.
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import sys
import os

# Set the path to the Tesseract executable (adjust if necessary on Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_with_ocr(image_path, lang="fas+ara+eng"):
    """
    Extract text from an image using Tesseract OCR.

    Parameters:
        image_path (str): The path to the image file.
        lang (str): Languages to be used for OCR (e.g., 'fas+ara+eng').

    Returns:
        str: Extracted text from the image, or an empty string in case of an error.
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
    Create an output folder based on the PDF file name.
    The folder will be created in the same directory as the script.

    Parameters:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The path to the created output folder.

    Raises:
        Exception: If there is an error creating the folder.
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
    Process a PDF file by extracting text and saving each page as an image.

    For each page in the PDF:
      - Attempts to extract text using PyMuPDF's get_text() method.
      - Renders the page as an image and saves it as a PNG file.
      - If the extracted text is insufficient (less than 30 characters), uses OCR (Tesseract)
        on the saved image.
      - Saves the final extracted text into a .txt file.
    All outputs are saved in an output folder created based on the PDF file name.

    Parameters:
        pdf_path (str): Path to the PDF file.
        ocr_lang (str): Languages used for OCR (default is 'fas+ara+eng').
        zoom_factor (int): Zoom factor for rendering the page (affects image resolution for OCR).

    Returns:
        None
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
        
        # Set filenames for the text and image outputs
        text_filename = os.path.join(output_folder, f"page_{page_number + 1}.txt")
        image_filename = os.path.join(output_folder, f"page_{page_number + 1}.png")
        
        # Render the page as an image (for saving and OCR)
        try:
            mat = fitz.Matrix(zoom_factor, zoom_factor)
            pix = page.get_pixmap(matrix=mat)
            pix.save(image_filename)
            print(f"Page {page_number + 1} image saved in file '{image_filename}'.")
        except Exception as e:
            print(f"Error rendering or saving image for page {page_number + 1}: {e}")
            continue
        
        # If the text extraction result is too short, use OCR to extract text from the image
        if len(extracted_text.strip()) < 30:
            print(f"Page {page_number + 1}: Text not found or too little. Using OCR...")
            extracted_text = extract_text_with_ocr(image_filename, lang=ocr_lang)
        
        # Save the extracted text into a .txt file
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
    Check if the PDF file and its directory exist, then process the PDF.

    Parameters:
        pdf_path (str): The path to the PDF file.

    Returns:
        None
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
