import streamlit as st
from PIL import Image
import base64
import os
import io

st.set_page_config(layout="wide")

def get_base64_image(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Klasörü oluştur
if not os.path.exists("images"):
    os.makedirs("images")

bg_path = "images/backG1.jpg"

# Görsel yükleme
st.sidebar.markdown("## 🎨 Arka Plan Ayarı")
bg_file = st.sidebar.file_uploader("Bir görsel yükle (PNG, JPG)", type=["png", "jpg", "jpeg"])

if bg_file:
    img = Image.open(bg_file)
    img.save(bg_path)
    st.sidebar.success("✅ Arka plan kaydedildi!")

# Eğer arka plan varsa, base64 ile CSS'e göm
if os.path.exists(bg_path):
    b64_bg = get_base64_image(bg_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .block-container {{
        background-color: rgba(0,0,0,0.6);
        padding: 2rem;
        border-radius: 12px;
    }}
    h1, h2, h3 {{
        color: white;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.info("ℹ️ Henüz arka plan yüklenmedi.")

# Örnek içerik
st.title("KALEVERİ")
st.write("Bu metin yüklediğin görselin önünde görünür.")
