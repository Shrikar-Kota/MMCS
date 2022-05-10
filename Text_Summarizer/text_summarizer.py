from summarizer import TransformerSummarizer
from transformers import logging

from .save_summary_to_file import save_summary_to_file

logging.set_verbosity_error()

def getTextSummary(body, OUTPUT_PATH, fileid, emailhash):
    model = TransformerSummarizer(transformer_type="XLNet",transformer_model_key="xlnet-base-cased")
    summary = ''.join(model(body, min_length=60))
    print("Genereted textual summary: \n", summary, "\n\n\n")
    save_summary_to_file(summary, OUTPUT_PATH, fileid, emailhash)