import google.generativeai as genai
import streamlit as st
from PIL import Image
import io

# ตั้งค่าหน้า UI
st.set_page_config(page_title="AI Image Keyword Generator", layout="centered")

# ส่วนหัวของแอป
st.title("🔍 AI Image Keyword Generator")
st.write("อัปโหลดรูปภาพ แล้วให้ AI สร้างคีย์เวิร์ดสำหรับค้นหารูปที่คล้ายกัน!")

# โหลดค่า Environment Variables จาก Streamlit Secrets
GENAI_API_KEY = st.secrets["GENAI"]["api_key"]

# ตรวจสอบค่า Environment Variables
if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY is not set in Streamlit secrets.")

# ตั้งค่า Gemini AI API
genai.configure(api_key=GENAI_API_KEY)

def generate_keywords_from_image(image_file):
    """ใช้ Gemini วิเคราะห์ภาพและสร้างคีย์เวิร์ด"""
    if image_file is None:
        raise ValueError("❌ No image file provided.")

    # แปลง uploaded file (BytesIO) เป็น PIL image
    image = Image.open(image_file)

    # ✅ ใช้โมเดล gemini-pro-vision ที่รองรับภาพ
    model = genai.GenerativeModel("gemini-2.5-Pro")
    response = model.generate_content(
        [image, "Can you suggest some keywords to search for similar images for design reference?"]
    )

    # ตรวจสอบ response และดึงคีย์เวิร์ด
    if response and hasattr(response, 'text'):
        keywords = response.text.strip().split(", ")
    else:
        keywords = ["No keywords generated."]

    return keywords
    
# อัปโหลดไฟล์รูปภาพ
uploaded_file = st.file_uploader("📤 อัปโหลดรูปภาพที่ต้องการวิเคราะห์", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:

    # แสดงภาพที่อัปโหลด
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 รูปที่อัปโหลด", use_column_width=True)

    
    # ปุ่มวิเคราะห์
    if st.button("🔍 สร้างคีย์เวิร์ด"):
        with st.spinner("AI กำลังวิเคราะห์... ⏳"):
            keywords = generate_keywords_from_image(uploaded_file)

        st.subheader("🔑 คีย์เวิร์ดที่ได้:")
        st.write(", ".join(keywords))
