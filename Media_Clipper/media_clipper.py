from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import pathlib

def clip_video_file(start, end, fileid, extension, MEDIA_PATH):
    clip = VideoFileClip(MEDIA_PATH)
    clip = clip.subclip(start, end)
    NEW_MEDIA_PATH = os.path.join(pathlib.Path(MEDIA_PATH).parent, f"{fileid}_clipped.{extension}")
    clip.write_videofile(NEW_MEDIA_PATH)
    clip.close()
    os.remove(MEDIA_PATH)
    os.rename(NEW_MEDIA_PATH, MEDIA_PATH)
    print("Video trimmed\n\n")
    
    
def clip_audio_file(start, end, fileid, extension, MEDIA_PATH):
    song = AudioSegment.from_file(MEDIA_PATH)
    extract = song[start*1000:end*1000]
    NEW_MEDIA_PATH = os.path.join(pathlib.Path(MEDIA_PATH).parent, f"{fileid}_clipped.{extension}")
    extract.export(NEW_MEDIA_PATH, format=extension)
    os.remove(MEDIA_PATH)
    os.rename(NEW_MEDIA_PATH, MEDIA_PATH)
    print("Audio trimmed\n\n")
    
def clip_media_file(start, end, fileid, extension, MEDIA_PATH, FILE_TYPE):
    if FILE_TYPE == 'VIDEO':
        clip_video_file(start, end, fileid, extension, MEDIA_PATH)
    else:
        clip_audio_file(start, end, fileid, extension, MEDIA_PATH)
    
    return True