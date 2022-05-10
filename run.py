import os
from pathlib import Path
import time

from Summarizer_Server import generate_summary

print("Started Serving")

while 1:
    generate_summary()
    time.sleep(60)