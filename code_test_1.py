import fitz  # PyMuPDF
import sys
import os

def process_pdf(pdf_path):
    # باز کردن فایل PDF
    doc = fitz.open(pdf_path)
    
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        
        # استخراج متن صفحه
        text = page.get_text("text")
        text_filename = f"page_{page_number + 1}.txt"
        with open(text_filename, "w", encoding="utf-8") as text_file:
            text_file.write(text)
        print(f"Content of the page {page_number + 1} saved into '{text_filename}'")
        
        # رندر کردن صفحه به تصویر PNG
        zoom = 2  # می‌توانید این مقدار را برای افزایش کیفیت تصویر تغییر دهید
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        image_filename = f"page_{page_number + 1}.png"
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
    pdf_path = r"D:\\workspace\\test_enviroment\\convert_pdf_to_image\\pdfs\\c.pdf"
    
    check_and_process_pdf(pdf_path)
    
