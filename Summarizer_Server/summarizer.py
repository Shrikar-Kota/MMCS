from ..Client_Server.summarizer.models import MediaDetails
from .generate_text_summary import generate_text_summary
from .generate_audio_summary import generate_audio_summary
from .generate_video_summary import generate_video_summary
from pathlib import Path
import os
import hashlib

def generate_summary():
    media_data = MediaDetails.getOldestRequest()
    if not media_data:
        return
    emailhash = hashlib.md5(media_data.user.email.encode()).hexdigest()
    MediaDetails.updateStatus(media_data['user'], media_data['fileid'], 'QUEUED')
    if media_data['type'] == 'TEXT':
        INPUT_PATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(Path(os.getcwd).parent, 'Media'), media_data['email_hash']), 'INPUT'), 'TEXT'), f"{media_data['fileid']}.{media_data['filextension']}")
        generate_text_summary(INPUT_PATH, emailhash, media_data)
        
    elif media_data['type'] == 'AUDIO':
        INPUT_PATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(Path(os.getcwd).parent, 'Media'), media_data['email_hash']), 'INPUT'), 'AUDIO'), f"{media_data['fileid']}.{media_data['filextension']}")
        generate_audio_summary(INPUT_PATH, emailhash, media_data)
        
    else:
        INPUT_PATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(Path(os.getcwd).parent, 'Media'), media_data['email_hash']), 'INPUT'), 'VIDEO'), f"{media_data['fileid']}.{media_data['filextension']}")
        generate_video_summary(INPUT_PATH, emailhash, media_data)
    
    MediaDetails.updateStatus(media_data['user'], media_data['fileid'], 'FINISHED')
    
    return True