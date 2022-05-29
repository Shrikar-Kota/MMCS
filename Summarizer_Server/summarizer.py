from datetime import datetime
from .generate_text_summary import generate_text_summary
from .generate_audio_summary import generate_audio_summary
from .generate_video_summary import generate_video_summary
from .interact import getOldestRequest, updateStatus
from Media_Clipper import clip_media_file

from pathlib import Path
import os
import hashlib

from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def generate_summary():
    media_data = getOldestRequest()
    if not media_data:
        print("No media found")
        return
    print("Data Found")

    emailhash = hashlib.md5(media_data['email'].encode()).hexdigest()
    updateStatus(email=media_data['email'], fileid=media_data['fileid'], status='PROCESSING')
    if media_data['filetype'] == 'TEXT':
        INPUT_PATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(os.getcwd(), 'Media'), emailhash), 'INPUT'), 'TEXT'), f"{media_data['fileid']}.{media_data['fileextension']}")
        generate_text_summary(INPUT_PATH, emailhash=emailhash, **media_data)
        
    elif media_data['filetype'] == 'AUDIO':
        INPUT_PATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(os.getcwd(), 'Media'), emailhash), 'INPUT'), 'AUDIO'), f"{media_data['fileid']}.{media_data['fileextension']}")
        if media_data['start_time_of_media'] != 0 and media_data['end_time_of_media'] != get_duration_of_media(INPUT_PATH, 'AUDIO'):
            clip_media_file(media_data['start_time_of_media'], media_data['end_time_of_media'], media_data['fileid'], media_data['fileextension'], INPUT_PATH, 'AUDIO')
        generate_audio_summary(INPUT_PATH, emailhash=emailhash, **media_data)
    else:
        INPUT_PATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(os.getcwd(), 'Media'), emailhash), 'INPUT'), 'VIDEO'), f"{media_data['fileid']}.{media_data['fileextension']}")
        if media_data['start_time_of_media'] != 0 and media_data['end_time_of_media'] != get_duration_of_media(INPUT_PATH, 'VIDEO'):
            if clip_media_file(media_data['start_time_of_media'], media_data['end_time_of_media'], media_data['fileid'], media_data['fileextension'], INPUT_PATH, 'VIDEO'):
                generate_video_summary(INPUT_PATH, emailhash=emailhash, **media_data)
    
    updateStatus(email=media_data['email'], fileid=media_data['fileid'], status='FINISHED')
    return True

def get_duration_of_media(INPUT_FILE_PATH, MEDIA_TYPE):
    if MEDIA_TYPE == 'VIDEO':
        clip = VideoFileClip(INPUT_FILE_PATH)
        return int(clip.duration)
    else:
        audio = AudioSegment.from_file(INPUT_FILE_PATH)
        return int(audio.duration_seconds)