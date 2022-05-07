from mimetypes import suffix_map
import os
from tkinter import filedialog
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
from pathlib import Path
import Katna.config as config
from Katna.mediapipe import MediaPipeAutoFlip
from multiprocessing import cpu_count
import Katna.helper_functions as helper

class KeyFrameExtractor(KeyFrameDiskWriter):
    def generate_output_filename(self, filepath, keyframe_number):
        suffix = str(keyframe_number)
        return super().generate_output_filename(filepath, suffix)
        
class Video1(Video):
    def __init__(self, autoflip_build_path=None, autoflip_model_path=None, clip_path=None):
        helper._set_ffmpeg_binary_path()
        # If the duration of the clipped video is less than **min_video_duration**
        # then, the clip will be added with the previous clipped
        self._min_video_duration = config.Video.min_video_duration

        # Calculating optimum number of processes for multiprocessing
        self.n_processes = cpu_count() // 2 - 1
        if self.n_processes < 1:
            self.n_processes = None

        if autoflip_build_path is not None and autoflip_model_path is not None:
            self.mediapipe_autoflip = MediaPipeAutoFlip(
                autoflip_build_path, autoflip_model_path
            )
        else:
            self.mediapipe_autoflip = None
            
        self.temp_folder = os.path.abspath(os.path.join("clipped")) if clip_path is None else clip_path
        if not os.path.isdir(self.temp_folder):
            os.makedirs(self.temp_folder)

def extractKeyFrames(FILE_PATH, fileid, emailhash):
    OUTPUT_PATH = os.path.join(Path(FILE_PATH).parent.parent.parent.parent, "Key_Frame_Extractor_Media")
    OUTPUT_PATH = os.path.join(os.path.join(OUTPUT_PATH, emailhash), fileid)
    vd = Video1(clip_path = os.path.join(OUTPUT_PATH, 'clipped'))
    diskwriter = KeyFrameExtractor(location=OUTPUT_PATH)
    vd.extract_video_keyframes(
        no_of_frames=15, file_path=FILE_PATH,
        writer=diskwriter
    )
    return OUTPUT_PATH

if __name__ == '__main__':
    def extract_key_frames_from_video(FILE_PATH, fileid, emailhash):
        return extractKeyFrames(FILE_PATH, fileid, emailhash)
    print(extract_key_frames_from_video("D:/Shrikar/Projects/Multimedia_Summarization/Project/Code/Media/36f05f601808a523f6bad7751af46499/INPUT/VIDEO/abc.mp4", "172381263378126", "djhakjhdkjshdkjhaj"))
