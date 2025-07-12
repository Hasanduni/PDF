import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyABcgB6_ekXpU1FffEt9ANh2fLEMWRbLu8"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Streamlit UI
st.set_page_config(page_title="PDF Summarizer with Gemini", layout="wide")
st.title("📄 PDF Summarizer using Gemini AI")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        pdf_text = extract_text_from_pdf("temp.pdf")

    st.success("✅ Text extracted!")
    st.subheader("Preview of Extracted Text")
    st.text_area("Text Preview", pdf_text[:1000], height=200)

    if st.button("Generate Summary"):
        with st.spinner("Generating summary using Gemini..."):
            response = model.generate_content(
                f"Summarize this PDF document:\n\n{pdf_text[:20000]}"
            )
        st.success("✅ Summary generated!")
        st.subheader("Summary")
        st.write(response.text)
