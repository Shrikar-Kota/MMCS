from .key_frame_extractor import extractKeyFrames

def extract_key_frames_from_video(INPUT_PATH, fileid, emailhash):
    return extractKeyFrames(INPUT_PATH, fileid, emailhash)