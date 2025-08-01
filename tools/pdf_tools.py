import PyPDF2
import io
import os

def extract_text_from_pdf(filepath: str) -> str:
    """Extracts text from a PDF file.

    Args:
        filepath (str): The path to the PDF file.

    Returns:
        str: The extracted text, or an error message.
    """
    if not os.path.exists(filepath):
        return f"Error: The file at {filepath} was not found."

    try:
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        return f"An error occurred while extracting text from the PDF: {e}"