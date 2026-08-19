import os
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Compliance Checker", layout="wide")
st.title("🛡️ AI-Powered Compliance Review Tool")

# Read API Key securely from cloud secrets or manual input
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# User input text area
user_input = st.text_area(
    "Enter text, policies, or communications to analyze:",
    height=200,
    placeholder="Paste text here...",
)

if st.button("Run Compliance Analysis"):
    if not api_key:
        st.error("Please provide a valid Gemini API key.")
    elif not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing against compliance standards..."):
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an expert compliance auditor. Analyze the following submission:
            
            ---
            {user_input}
            ---
            
            Provide:
            1. Risk Level (Low / Medium / High)
            2. Policy Violations or Issues Detected
            3. Recommended Corrections / Rewrites
            """
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
            )
            st.subheader("Analysis Results")
            st.markdown(response.text)