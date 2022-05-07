from doctest import OutputChecker
import moviepy.editor as mp
import os
from pathlib import Path
def get_audio_from_video(FILE_SOURCE, fileid, emailhash):
    my_clip = mp.VideoFileClip(FILE_SOURCE)
    OUTPUT_SOURCE = os.path.join(os.path.join(Path(FILE_SOURCE).parent.parent.parent.parent, "AV_Separator_Media"), f"{emailhash}_{fileid}.wav")
    my_clip.audio.write_audiofile(OUTPUT_SOURCE)
    return OUTPUT_SOURCE
