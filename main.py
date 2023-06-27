import cv2
import numpy as np
import pdf2image
import pytesseract
from tkinter import Tk, filedialog

def convert_pdf_to_img(file_obj, dpi):
        try:
            with open(file_obj, 'rb') as f:
                for image in pdf2image.convert_from_bytes(f.read(), dpi=dpi):
                    yield cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f'Error converting PDF to images: {e}', 'error')

def process_file(file_path):
    lines = []
    for image in convert_pdf_to_img(file_path, 400):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        document_text = pytesseract.image_to_string(gray)
        for line in document_text.split('\n'):
            if line != '':
                lines.append(line)

    # Create a text file and write each line as a separate item in the array
    output_file = file_path.replace('.pdf', '.txt')
    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    print(f'Content extracted and saved to {output_file}')
            
def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        process_file(file_path)
        
if __name__ == '__main__':
    select_file()