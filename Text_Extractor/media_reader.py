from .get_text_from_pdf import get_text_from_pdf
from .get_text_from_word import get_text_from_doc, get_text_from_word
from .get_text_from_txt import get_text_from_txt
from .get_text_from_audio import get_text_from_audio

def extract_text_from(INPUT_PATH, extension, fileid, emailhash, from_video=False):
    textout = ""
    if extension == 'pdf':
        textout = get_text_from_pdf(INPUT_PATH)
    elif extension == 'doc':
        textout = get_text_from_doc(INPUT_PATH)
    elif extension == 'docx':
        textout = get_text_from_word(INPUT_PATH)
    elif extension == 'txt':
        textout = get_text_from_txt(INPUT_PATH)
    else:
        textout = get_text_from_audio(INPUT_PATH, extension, fileid, emailhash, from_video)
    return textout
