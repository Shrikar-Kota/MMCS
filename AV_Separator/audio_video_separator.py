import moviepy.editor as mp
import os
from pathlib import Path
def get_audio_from_video(INPUT_PATH, fileid, emailhash):
    my_clip = mp.VideoFileClip(INPUT_PATH)
    OUTPUT_SOURCE = os.path.join(os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "AV_Separator_Media"), f"{emailhash}_{fileid}.wav")
    my_clip.audio.write_audiofile(OUTPUT_SOURCE)
    my_clip.close()