"""
Author: Rohini
Email: rolearnings@yahoo.com
Date: 2025-10-10
Description: This script intened to have chat from the UI using streamlit
"""

from PyPDF2 import PdfReader
from ssb_exceptions import InvalidInputError

def extract_text_from_pdf(input_folder_path : str, write_file_name: str) -> str:
    """
    For the provided input pdf data path, data are extracted page by page and
    stored it as plain text in staging data folder

    Args:
        input_folder_path (str): ssb input data folder path
        write_file_name (str): ssb staging data folder path

    Returns:
        str: ssb staging data folder path
    """

    if not isinstance(input_folder_path, str):
        raise InvalidInputError("Pass on file path as string")
    
    try:
        reader = PdfReader(input_folder_path)
    except FileNotFoundError as fe:
        print(f"Input file {input_folder_path} not found !! {fe}")
        
    try:
        text = "\n".join(page.extract_text() for page in reader.pages)
        with open(write_file_name, "w") as f:
            f.write(text)
        return write_file_name
    except EOFError as ef:
        print(f"Error extracting pdf data {ef}")
    
if __name__ == "__main__":
    
    input_folder_path = "data/saisatcharita/Sri-Sai-Satcharitra-English.pdf"
    write_file_name = "data/staging_data/Sri-Sai-Satcharitra-English.txt"
    extract_text_from_pdf(input_folder_path=input_folder_path, write_file_name=write_file_name)
        
