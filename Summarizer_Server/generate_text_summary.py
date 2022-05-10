from Text_Summarizer import getTextSummary
from Text_Extractor import extract_text_from
from PDF_Generator import generate_summary_pdf

from pathlib import Path
import os

def generate_text_summary(INPUT_PATH, emailhash, **kwargs):
    text = extract_text_from(INPUT_PATH, kwargs['fileextension'], kwargs['fileid'], emailhash)
    OUTPUT_PATH = os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "Text_Summarizer_Media")
    getTextSummary(text, OUTPUT_PATH, kwargs['fileid'], emailhash)
    SUMMARY_PATH = os.path.join(OUTPUT_PATH, f"{emailhash}_{kwargs['fileid']}.txt")
    generate_summary_pdf(SUMMARY_PATH, emailhash, kwargs['fileid'])
    os.remove(SUMMARY_PATH)
    os.remove(INPUT_PATH)

    