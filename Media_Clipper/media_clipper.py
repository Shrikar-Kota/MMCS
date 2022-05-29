from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import pathlib

def clip_video_file(start, end, fileid, extension, MEDIA_PATH):
    clip = VideoFileClip(MEDIA_PATH)
    clip = clip.subclip(start, end)
    clip.write_videofile(MEDIA_PATH)
    clip.close()
    print("Video trimmed\n\n")
    
    
def clip_audio_file(start, end, fileid, extension, MEDIA_PATH):
    song = AudioSegment.from_file(MEDIA_PATH)
    extract = song[start*1000:end*1000]
    extract.export(MEDIA_PATH, format=extension)
    os.rename(MEDIA_PATH, MEDIA_PATH)
    print("Audio trimmed\n\n")
    
def clip_media_file(start, end, fileid, extension, MEDIA_PATH, FILE_TYPE):
    if FILE_TYPE == 'VIDEO':
        clip_video_file(start, end, fileid, extension, MEDIA_PATH)
    else:
        clip_audio_file(start, end, fileid, extension, MEDIA_PATH)
    
    return True