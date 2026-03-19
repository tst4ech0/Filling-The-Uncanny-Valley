import os
from docx import Document
import pdfplumber

def read_file(file):
    """
    Read text from uploaded file.
    Supports .txt, .docx, and .pdf files.
    
    Args:
        file: Flask file upload object
        
    Returns:
        tuple: (text content as string, error message if any)
    """
    filename = file.filename.lower()
    
    # Check file extension
    if filename.endswith('.txt'):
        try:
            text = file.read().decode('utf-8')
            return text, None
        except Exception as e:
            return None, f"Error reading .txt file: {str(e)}"
    
    elif filename.endswith('.docx'):
        try:
            # Save temporarily to read with python-docx
            temp_path = 'temp_upload.docx'
            file.save(temp_path)
            
            # Extract text from docx
            doc = Document(temp_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            
            # Clean up temp file
            os.remove(temp_path)
            
            return text, None
        except Exception as e:
            # Clean up temp file if it exists
            if os.path.exists('temp_upload.docx'):
                os.remove('temp_upload.docx')
            return None, f"Error reading .docx file: {str(e)}"
    
    elif filename.endswith('.pdf'):
        try:
            # Save temporarily to read with pdfplumber
            temp_path = 'temp_upload.pdf'
            file.save(temp_path)
            
            # Extract text from PDF
            text = ""
            with pdfplumber.open(temp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
            
            # Clean up temp file
            os.remove(temp_path)
            
            if not text.strip():
                return None, "PDF appears to be empty or contains only images"
            
            return text, None
        except Exception as e:
            # Clean up temp file if it exists
            if os.path.exists('temp_upload.pdf'):
                os.remove('temp_upload.pdf')
            return None, f"Error reading .pdf file: {str(e)}"
    
    else:
        return None, "Unsupported file type. Please use .txt, .docx, or .pdf files."