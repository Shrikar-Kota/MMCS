from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment
import os
import pathlib

def clip_video_file(start, end, fileid, extension, MEDIA_PATH):
    new_name = os.path.join(pathlib.Path(MEDIA_PATH).parent, fileid+"_full."+extension)
    os.rename(MEDIA_PATH, new_name)
    ffmpeg_extract_subclip(new_name, start, end, targetname=MEDIA_PATH)
    os.remove(new_name)
    print("Video trimmed\n\n")
    
    
def clip_audio_file(start, end, extension, MEDIA_PATH):
    song = AudioSegment.from_file(MEDIA_PATH)
    extract = song[start*1000:end*1000]
    extract.export(MEDIA_PATH, format=extension)
    os.rename(MEDIA_PATH, MEDIA_PATH)
    print("Audio trimmed\n\n")
    
def clip_media_file(start, end, fileid, extension, MEDIA_PATH, FILE_TYPE):
    if FILE_TYPE == 'VIDEO':
        clip_video_file(start, end, fileid, extension, MEDIA_PATH)
    else:
        clip_audio_file(start, end, extension, MEDIA_PATH)
    
    return True