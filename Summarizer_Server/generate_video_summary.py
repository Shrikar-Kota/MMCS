from ..AV_Separator import get_audio_from_video
from ..Text_Summarizer import text_summarizer
from ..Text_Extractor import media_reader
from ..Key_Frame_Extractor import extract_key_frames_from_video
from ..PDF_Generator import generate_summary_pdf


import os
from pathlib import Path


def generate_video_summary(INPUT_PATH, **kwargs):
    get_audio_from_video(INPUT_PATH, fileid, emailhash)
    AUDIO_PATH = os.path.join(os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "AV_Separator_Media"), f"{emailhash}_{fileid}.wav")
    text = media_reader(AUDIO_PATH, fileextension, fileid, emailhash)
    TEXT_SUMMARY_PATH = os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "Text_Summarizer_Media")
    text_summarizer(text, TEXT_SUMMARY_PATH, fileid, emailhash)
    TEXT_SUMMARY_PATH = os.path.join(TEXT_SUMMARY_PATH, f"{emailhash}_{fileid}.txt")
    extract_key_frames_from_video(INPUT_PATH, fileid, emailhash)
    KEY_FRAMES_PATH = os.path.join(os.path.join(os.path.join(Path(INPUT_PATH).parent.parent.parent, "KeY_Frame_Extractor_Media"), emailhash, fileid))
    generate_summary_pdf(SUMMARY_PATH, emailhash, fileid, KEY_FRAMES_PATH)
    os.remove(TEXT_SUMMARY_PATH)
    os.remove(AUDIO_PATH)
    os.rmdir(KEY_FRAMES_PATH)
    