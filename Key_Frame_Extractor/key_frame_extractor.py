import os
from datetime import datetime
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
if __name__ == "__main__":
    vd = Video()
    start = datetime.now()
    FILE_PATH = os.path.join(os.getcwd(), 'TEST.mp4')
    OUTPUT_PATH = os.path.join(os.getcwd(), 'result')
    diskwriter = KeyFrameDiskWriter(location=OUTPUT_PATH)
    vd.extract_video_keyframes(
        no_of_frames=30, file_path=FILE_PATH,
        writer=diskwriter
    )