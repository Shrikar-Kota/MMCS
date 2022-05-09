from .generate_text_summary import generate_text_summary

def generate_audio_summary(INPUT_PATH, **kwargs):
    generate_text_summary(INPUT_PATH, **kwargs)