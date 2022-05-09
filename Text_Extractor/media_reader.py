from .get_text_from_pdf import *
from .get_text_from_word import *
from .get_text_from_txt import *
from .get_text_from_audio import *

def extract_text_from(INPUT_PATH, extension, **kwargs):
    textout = ""
    if extension == 'pdf':
        textout = get_text_from_pdf(INPUT_PATH)
    if extension == 'doc':
        textout = get_text_from_doc(INPUT_PATH)
    if extension == 'docx':
        textout = get_text_from_word(INPUT_PATH)
    if extension == 'txt':
        textout = get_text_from_txt(INPUT_PATH)
    else:
        textout = get_text_from_audio(INPUT_PATH, **kwargs)
    return textout
