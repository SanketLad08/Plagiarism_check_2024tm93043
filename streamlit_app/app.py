# streamlit_app/app.py
#import sys, os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "../flask_api")))

import streamlit as st
import requests
import os

st.set_page_config(page_title="Plagiarism Checker", layout="wide")
st.title("📄 Plagiarism Checker (Streamlit UI)")

st.markdown("Upload original and submission text files. This frontend calls the Flask API at http://localhost:5000/check")

col1, col2 = st.columns(2)
with col1:
    original_file = st.file_uploader("Upload Original File", type=["txt"], key="orig")
with col2:
    submission_file = st.file_uploader("Upload Submission File", type=["txt"], key="sub")

if st.button("Check Plagiarism"):
    if not original_file or not submission_file:
        st.error("Please upload both files.")
    else:
        files = {
            "original": original_file,
            "submission": submission_file
        }
        try:
            response = requests.post("http://localhost:5000/check", files=files, timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.metric("Similarity Score", f"{data['similarity_score']*100:.2f}%")
                st.metric("Plagiarism Probability", f"{data['probability']*100:.2f}%")
                if data["plagiarized"]:
                    st.error("🔴 This submission is likely plagiarized.")
                else:
                    st.success("🟢 This submission seems original.")

                st.markdown("### 🔍 Highlighted Matches in Original")
                st.markdown(data["highlighted_original"], unsafe_allow_html=True)

                st.markdown("### 🔍 Highlighted Matches in Submission")
                st.markdown(data["highlighted_submission"], unsafe_allow_html=True)
            else:
                st.error(f"API error: {response.status_code} {response.text}")
        except Exception as e:
            st.error(f"Connection failed: {e}")
