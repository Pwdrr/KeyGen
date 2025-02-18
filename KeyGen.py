import google.generativeai as genai
import streamlit as st
from PIL import Image

# โหลดค่า Environment Variables จาก Streamlit Secrets
GENAI_API_KEY = st.secrets["GENAI"]["api_key"]

# ตรวจสอบค่า Environment Variables
if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY is not set in Streamlit secrets.")

# ตั้งค่า Gemini AI API
genai.configure(api_key=GENAI_API_KEY)

def generate_keywords_from_image(image_path):
    """ใช้ Gemini วิเคราะห์ภาพและสร้างคีย์เวิร์ด"""
    model = genai.GenerativeModel("gemini-pro-vision")
    image = Image.open(image_path)

    response = model.generate_content(
        ["Can you suggest some keywords to search for similar images for design reference?"],
        image=image
    )

    keywords = response.text.strip().split(", ")
    return keywords
