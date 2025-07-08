import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import time
from summarizer import summarize_text
import os

# Set path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Page config
st.set_page_config(page_title="AI Notes & PDF Summarizer", layout="centered")

# Theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "light"

theme = st.session_state.theme
if theme == "dark":
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #0e1117;
            color: white;
        }
        .stTextInput, .stTextArea, .stFileUploader, .stButton {
            background-color: #262730;
            color: white;
        }
        .stTextArea > div > textarea {
            background-color: #1c1c1c !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #ffffff;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

# Title and toggle button
st.title("🧠 AI Notes & PDF Summarizer")
toggle = "🌙 Dark Mode" if theme == "light" else "☀️ Light Mode"
if st.button(toggle, key="theme-toggle"):
    st.session_state.theme = "dark" if theme == "light" else "light"
    st.rerun()

# Upload or manual input
uploaded_file = st.file_uploader("📤 Upload PDF or TXT", type=["pdf", "txt"], key="file-upload")

manual_text = ""
show_manual = st.checkbox("📝 I want to type or paste text instead", key="manual_toggle")
if show_manual:
    manual_text = st.text_area("Paste your text here:", height=200)

# OCR for PDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for i, page in enumerate(doc):
            if i >= 5:
                break
            img = page.get_pixmap()
            img_bytes = img.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))
            text += pytesseract.image_to_string(image) + "\n"
    return text

# Extract input text
full_text = ""
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        full_text = extract_text_from_pdf(uploaded_file)
    else:
        full_text = uploaded_file.read().decode("utf-8")
elif manual_text.strip():
    full_text = manual_text

# Summarize
if full_text.strip():
    st.subheader("✨ Ready to Summarize?")
    if st.button("Summarize", key="summarize-btn"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(full_text)

        st.success("🎯 Gotcha! Here's your summarized version ↓")

        points = [line.strip() for line in summary.split(".") if len(line.strip()) > 0]
        final_summary = ""
        for point in points:
            bullet = f"• {point.strip().replace('Asticial', 'Artificial').replace('LI', 'AI').replace('Al', 'AI')}."
            st.markdown(bullet)
            final_summary += bullet + "\n"
            time.sleep(0.25)

        st.download_button("📥 Download Summary", final_summary, file_name="summary.txt")
else:
    st.info("⬆️ Upload a file or paste text to get started.")
