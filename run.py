import os
from pathlib import Path
import time

from Summarizer_Server import generate_summary

print("Started Serving")

p = os.path.join(os.getcwd(), "Media")
for filename in ["AV_Separator_Media", "Key_Frame_Extractor_Media", "Text_Extractor_Media", "Text_Summarizer_Media"]:
    try:
        os.makedirs(os.path.join(p, filename))
    except:
        pass
print("Created MetaData Files")

while 1:
    generate_summary()
    time.sleep(60)