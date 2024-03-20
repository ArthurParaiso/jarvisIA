import fitz  # PyMuPDF
import os


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Parameters:
    - pdf_path: Path to the PDF file.

    Returns:
    - extracted_text: The extracted text as a string.
    """
    extracted_text = ''
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                extracted_text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
    return extracted_text


def extract_texts_from_folder(folder_path):
    """
    Extracts text from all PDF files in a specified folder.

    Parameters:
    - folder_path: Path to the folder containing PDF files.

    Returns:
    - texts: A list of extracted texts from all PDFs in the folder.
    """
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            texts.append(text)
    return texts


if __name__ == "__main__":
    folder_path = "./data/pdf_books/"
    texts = extract_texts_from_folder(folder_path)
    print("Extracted texts from PDFs.")
