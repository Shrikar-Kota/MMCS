from .get_text_from_pdf import *
from .get_text_from_word import *
from .get_text_from_txt import *
from .get_text_from_audio import *

def extract_text_from(FILE_PATH, extension):
    textout = ""
    if extension == 'pdf':
        textout = get_text_from_pdf(FILE_PATH)
    if extension == 'doc':
        textout = get_text_from_doc(FILE_PATH)
    if extension == 'docx':
        textout = get_text_from_word(FILE_PATH)
    if extension == 'txt':
        textout = get_text_from_txt(FILE_PATH)
    else:
        textout = get_text_from_audio(FILE_PATH)
    return textout
