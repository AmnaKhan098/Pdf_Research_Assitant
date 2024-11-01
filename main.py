import PyPDF2
import os
import streamlit as st
from groq import Groq

# Initialize Groq client using Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to summarize text using Groq
def summarize_text(text):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Summarize the following text: {text}"}],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

# Function to answer questions using Groq
def answer_question(question, context):
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"{context}\n\nAnswer the question: {question}"}
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

# Main function to process PDF
def process_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    summary = summarize_text(text)
    return summary, text

# Streamlit application
st.set_page_config(page_title="PDF QA Chatbot", page_icon="📄", layout="wide")
st.title("📄 PDF Question-Answer Chatbot")
st.markdown("<style>h1 {color: #2F4F4F;} h2 {color: #008080;} .footer {text-align: center; margin-top: 20px;}</style>", unsafe_allow_html=True)

# File uploader with styling
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", label_visibility="collapsed")

if uploaded_file is not None:
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Summary button
    if st.button("Generate Summary"):
        summary, extracted_text = process_pdf("uploaded.pdf")
        st.subheader("📋 PDF Summary")
        st.write(summary)
    
    # User question input with placeholder
    user_question = st.text_input("💬 Ask a question about the PDF:", placeholder="Type your question here...")

    if user_question and 'extracted_text' in locals():
        answer = answer_question(user_question, extracted_text)
        st.subheader("✅ Answer:")
        st.write(answer)






