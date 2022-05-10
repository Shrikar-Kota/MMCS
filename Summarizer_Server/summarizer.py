from .generate_text_summary import generate_text_summary
from .generate_audio_summary import generate_audio_summary
from .generate_video_summary import generate_video_summary
from .interact import getOldestRequest, updateStatus

from pathlib import Path
import os
import hashlib

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
        generate_audio_summary(INPUT_PATH, emailhash=emailhash, **media_data)
        
    else:
        INPUT_PATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(os.getcwd(), 'Media'), emailhash), 'INPUT'), 'VIDEO'), f"{media_data['fileid']}.{media_data['fileextension']}")
        generate_video_summary(INPUT_PATH, emailhash=emailhash, **media_data)
    
    updateStatus(email=media_data['email'], fileid=media_data['fileid'], status='FINISHED')
    
    return True