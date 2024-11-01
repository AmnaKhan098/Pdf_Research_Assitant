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

# Streamlit application
st.title("PDF Question-Answer Chatbot")
st.markdown("<h5 style='text-align: center;'>Upload a PDF and ask questions!</h5>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# To store summary and extracted text in session state
if "summary" not in st.session_state:
    st.session_state.summary = ""
    st.session_state.extracted_text = ""

if uploaded_file is not None:
    # Save the uploaded PDF to a file
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract text from PDF
    st.session_state.extracted_text = extract_text_from_pdf("uploaded.pdf")

# Summary button
if st.button("Generate Summary"):
    if st.session_state.extracted_text:
        st.session_state.summary = summarize_text(st.session_state.extracted_text)
        st.subheader("PDF Summary")
        st.write(st.session_state.summary)
    else:
        st.error("Please upload a PDF file first.")

# Create a text input for user questions
user_question = st.text_input("Ask a question about the PDF:")

if user_question and st.session_state.summary:
    answer = answer_question(user_question, st.session_state.extracted_text)
    st.subheader("Answer:")
    st.write(answer)

# Footer with your name
st.markdown("<footer style='text-align: center;'>Created by Amna Khan</footer>", unsafe_allow_html=True)


