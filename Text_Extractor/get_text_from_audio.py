import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
from pathlib import Path

r = sr.Recognizer()

def get_text_from_audio(INPUT_PATH, extension, fileid, emailhash, from_video):
    whole_text = ""
    if not from_video:
        folder_name = os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "Text_Extractor_Media")
    else:
        folder_name = os.path.join(Path(INPUT_PATH).parent.parent, "Text_Extractor_Media")
    sound = AudioSegment.from_file(INPUT_PATH, extension)
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence = 500,
    )
    
    target_length = 30 * 1000
    max_length = 40 * 1000
    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < target_length and len(output_chunks[-1]) + len(chunk) < max_length:
            output_chunks[-1] += chunk
        else:
            output_chunks.append(chunk)
            
    if len(output_chunks[-1]) > max_length:
        output_chunks = [*output_chunks[:-1], *make_chunks(output_chunks[-1], max_length)]
    for audio_chunk in output_chunks:
        chunk_filename = os.path.join(folder_name, f"{emailhash}_{fileid}_chunk.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            while 1:
                try:
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    break
                else:
                    text = f"{text.capitalize()}. "
                    whole_text += text
                    break
        os.remove(chunk_filename)
        
    print("Extracted text from audio: \n\n\n", whole_text, "\n\n\n")
    return whole_text