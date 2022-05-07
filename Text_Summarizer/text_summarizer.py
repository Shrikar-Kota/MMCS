from summarizer import TransformerSummarizer
from transformers import logging

logging.set_verbosity_error()

def getTextSummary(body):
    model = TransformerSummarizer(transformer_type="XLNet",transformer_model_key="xlnet-base-cased")
    full = ''.join(model(body, min_length=60))
    return full