from transformers import pipeline
from textblob import TextBlob
import re

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def clean_text(text):
    text = re.sub(r'[^A-Za-z0-9\s\.,;:\-\(\)\n]', '', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def correct_spelling(text):
    corrected = TextBlob(text).correct()
    return str(corrected).replace("Ll", "AI").replace("LI", "AI").replace("Al", "AI")

def summarize_text(text):
    text = clean_text(text)
    if len(text.split()) < 30:
        return "🤖 Not enough readable text found in your file. Please check the quality."
    if len(text.split()) > 512:
        text = " ".join(text.split()[:512])
    result = summarizer(text, max_length=150, min_length=30, do_sample=False)
    summary = result[0]['summary_text']
    return correct_spelling(summary)
