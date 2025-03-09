<<<<<<< HEAD
# Image_Text_extraction_from_PDF
Extract Image and Text from pdf file.
=======
# PDF Text and Image Extractor

This Python script processes a PDF file by extracting text and saving each page as an image. For every page in the PDF, the script:

- **Extracts text** using PyMuPDF.
- **Saves the page as a PNG image.**
- If the directly extracted text is insufficient (less than 30 characters), it falls back to **OCR extraction** using Tesseract (via the pytesseract library).
- **Stores the output** (both text and images) in an output folder created based on the PDF file name (without extension).

## Features

- **Dual extraction method:** Uses direct text extraction and falls back to OCR when necessary.
- **Automated output management:** Creates a dedicated folder for each PDF file’s outputs.
- **Error handling:** Implements try/except blocks to handle errors gracefully.

## Dependencies

The script requires the following Python libraries:

- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) – for processing PDFs.
- [pytesseract](https://pypi.org/project/pytesseract/) – Python wrapper for Tesseract OCR.
- [Pillow](https://python-pillow.org/) – for image processing.

### Installing Python Dependencies

Use `pip` to install the required libraries:

```bash
pip install pymupdf pytesseract Pillow
>>>>>>> 3088434 (Add docstring to code_test_tesseract_1.py and write README.md)
