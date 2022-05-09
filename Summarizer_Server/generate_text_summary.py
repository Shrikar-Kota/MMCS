from ..Text_Summarizer import text_summarizer
from ..Text_Extractor import media_reader
from ..PDF_Generator import generate_summary_pdf

from pathlib import Path
import os

def generate_text_summary(INPUT_PATH, **kwargs):
    text = media_reader(INPUT_PATH, fileextension, fileid, emailhash)
    OUTPUT_PATH = os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "Text_Summarizer_Media")
    text_summarizer(text, OUTPUT_PATH, fileid, emailhash)
    SUMMARY_PATH = os.path.join(OUTPUT_PATH, f"{emailhash}_{fileid}.txt")
    generate_summary_pdf(SUMMARY_PATH, emailhash, fileid)
    os.remove(SUMMARY_PATH)

    