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
st.title("PDF Question-Answer Chatbot")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    summary, extracted_text = process_pdf("uploaded.pdf")
    
    st.subheader("PDF Summary")
    st.write(summary)
    
    user_question = st.text_input("Ask a question about the PDF:")
    
    if user_question:
        answer = answer_question(user_question, extracted_text)
        st.subheader("Answer:")
        st.write(answer)

