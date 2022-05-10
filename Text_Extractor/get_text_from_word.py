from base64 import encode
from encodings import utf_8
import docx2txt
import win32com.client

def get_text_from_word(INPUT_PATH):
    text = docx2txt.process(INPUT_PATH)
    print("Extracted text from word: \n\n", text, "\n\n\n")
    return text

def get_text_from_doc(INPUT_PATH):
    word = win32com.client.Dispatch("Word.Application")
    word.visible = False
    wb = word.Documents.Open(INPUT_PATH)
    doc = word.ActiveDocument
    text = doc.Range().Text
    print("Extracted text from pdf: \n\n", text, "\n\n\n")
    wb.Close(True)
    return text