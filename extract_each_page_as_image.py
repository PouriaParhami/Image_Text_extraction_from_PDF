import fitz  # PyMuPDF
import sys
import os

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

def process_pdf(pdf_path):
    # باز کردن فایل PDF
    doc = fitz.open(pdf_path)
    
    output_folder = create_output_folder(pdf_path)
    
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        
        image_filename = os.path.join(output_folder, f"page_{page_number + 1}.png")
        
        # رندر کردن صفحه به تصویر PNG
        zoom = 2  # می‌توانید این مقدار را برای افزایش کیفیت تصویر تغییر دهید
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        pix.save(image_filename)
        print(f"Image of page {page_number + 1} saved in file '{image_filename}'")

    doc.close()
    
def check_and_process_pdf(pdf_path):
    
        folder_path = os.path.dirname(pdf_path)
        
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return
        
        if not os.path.exists(pdf_path):
            print(f"The file '{pdf_path}' does not exist.")
            return
        
        process_pdf(pdf_path)

if __name__ == "__main__":
    pdf_path = r"D:\\workspace\\test_enviroment\\convert_pdf_to_image\\pdfs\\a.pdf"
    
    check_and_process_pdf(pdf_path)
    
