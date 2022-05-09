import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pathlib import Path

r = sr.Recognizer()

def get_text_from_audio(INPUT_PATH, fileid, emailhash):
    whole_text = ""
    try:
        folder_name = os.path.join(Path(INPUT_PATH).parent.parent.parent.parent, "Text_Extractor_Media")
    
        sound = AudioSegment.from_file(INPUT_PATH, "wav")
        chunks = split_on_silence(sound,
            min_silence_len = 500,
            silence_thresh = sound.dBFS-14,
            keep_silence = 500,
        )
        
        target_length = 30 * 1000
        output_chunks = [chunks[0]]
        for chunk in chunks[1:]:
            if len(output_chunks[-1]) < target_length:
                output_chunks[-1] += chunk
            else:
                output_chunks.append(chunk)
        
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
    except:
        whole_text = "Something went wrong!"
    return whole_text