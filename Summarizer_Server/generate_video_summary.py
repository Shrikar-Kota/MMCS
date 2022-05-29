from AV_Separator import get_audio_from_video
from Text_Summarizer import getTextSummary
from Text_Extractor import extract_text_from
from Key_Frame_Extractor import extract_key_frames_from_video
from PDF_Generator import generate_summary_pdf


import os
from pathlib import Path
import shutil

def generate_video_summary(INPUT_PATH, **kwargs):
    get_audio_from_video(INPUT_PATH, kwargs['fileid'], kwargs['emailhash'])
    AUDIO_PATH = os.path.join(os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "AV_Separator_Media"), f"{kwargs['emailhash']}_{kwargs['fileid']}.wav")
    text = extract_text_from(AUDIO_PATH, kwargs['fileextension'], kwargs['fileid'], kwargs['emailhash'], from_video=True)
    TEXT_SUMMARY_PATH = os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "Text_Summarizer_Media")
    getTextSummary(text, TEXT_SUMMARY_PATH, kwargs['fileid'], kwargs['emailhash'])
    TEXT_SUMMARY_PATH = os.path.join(TEXT_SUMMARY_PATH, f"{kwargs['emailhash']}_{kwargs['fileid']}.txt")
    extract_key_frames_from_video(INPUT_PATH, kwargs['fileid'], kwargs['emailhash'], kwargs['nframes'])
    KEY_FRAMES_PATH = os.path.join(os.path.join(os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "Key_Frame_Extractor_Media"), kwargs['emailhash'], kwargs['fileid']))
    generate_summary_pdf(TEXT_SUMMARY_PATH, kwargs['emailhash'], kwargs['fileid'], KEY_FRAMES_PATH)
    os.remove(TEXT_SUMMARY_PATH)
    os.remove(AUDIO_PATH)
    shutil.rmtree(KEY_FRAMES_PATH)
    os.remove(INPUT_PATH)
    