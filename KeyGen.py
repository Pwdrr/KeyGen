import firebase_admin
from firebase_admin import credentials, firestore, storage
import google.generativeai as genai
import os
from dotenv import load_dotenv

from PIL import Image
import streamlit as st

# โหลดค่า Environment Variables
load_dotenv()


# ใช้ Environment Variables แทนค่าคงที่
FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS")
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")

# ตรวจสอบค่า Environment Variables
if not FIREBASE_CREDENTIALS:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is not set.")
if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY environment variable is not set.")

# เชื่อม Firebase
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'keygen-60990.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

print("Firestore Database Connected:", db)


# ตั้งค่า Gemini API
genai.configure(api_key=GENAI_API_KEY)

def upload_image_to_firebase(image_path):
    """อัปโหลดไฟล์ภาพไปยัง Firebase Storage และคืนค่า URL"""
    blob = bucket.blob(os.path.basename(image_path))
    blob.upload_from_filename(image_path)
    blob.make_public()  # ทำให้ URL ใช้งานได้
    return blob.public_url

def generate_keywords_from_image(image_path):
    """ใช้ Gemini วิเคราะห์ภาพและสร้างคีย์เวิร์ด"""
    model = genai.GenerativeModel("gemini-pro-vision")
    image = Image.open(image_path)

    response = model.generate_content(
        ["Can you suggest some keywords to search for similar images for design reference?:"],
        image=image
    )

    keywords = response.text.strip().split(", ")
    return keywords

def save_keywords_to_firestore(image_url, keywords):
    """บันทึกข้อมูลภาพและคีย์เวิร์ดลง Firestore"""
    doc_ref = db.collection("image_keywords").document()
    doc_ref.set({
        "image_url": image_url,
        "keywords": keywords
    })
    print("Saved to Firestore")

