import subprocess
import os
from pathlib import Path
import sys

def extract_key_frames_from_video(INPUT_PATH, fileid, emailhash, nframes): 
    p = subprocess.call(
            [sys.executable, os.path.join(os.path.join(Path(INPUT_PATH).parent.parent.parent.parent.parent, "Key_Frame_Extractor"), "extract_key_frames.py"), INPUT_PATH, fileid, emailhash, str(nframes)],
        )
    return