import docx2txt
import win32com.client

def get_text_from_word(FILE_PATH):
    text = docx2txt.process(FILE_PATH)
    return text

def get_text_from_doc(FILE_PATH):
    word = win32com.client.Dispatch("Word.Application")
    word.visible = False
    wb = word.Documents.Open(FILE_PATH)
    doc = word.ActiveDocument
    text = doc.Range().Text
    wb.Close(True)
    return text