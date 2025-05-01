# app.py
import io
import streamlit as st
import requests
import base64
import os
from PIL import Image
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px

from detection import detect_image_ai
from nightshade_wrap import poison_image
from detection_audio import detect_audio_ai
from kripto import encrypt_rgb_secret_into_rgb_carrier,decrypt_rgb_secret_from_carrier

# Sayfa Ayarı
st.set_page_config(page_title="KaleVeri", layout="wide", page_icon="🏰")

# --- Seçim Ekranı ---
if "page" not in st.session_state:
    st.session_state.page = None


def set_page(page_name):
    st.session_state.page = page_name

# Arka planı base64 formatına çevir
def get_base64_image(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Arka plan görseli yolu
background_path = "images/1.jpg"

# Arka plan sadece ana sayfada aktif
if st.session_state.page is None and os.path.exists(background_path):
    b64_bg = get_base64_image(background_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        background: transparent;
        padding-top: 2rem;
    }}

    .css-18e3th9 {{
        background: transparent;
    }}

    h1, h2, h3 {{
        color: white;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

if st.session_state.page is None:
    st.title("KALEVERİ")
    st.markdown("Yapay zeka tarafından üretilmiş görselleri analiz et veya kendi görselini manipülasyona karşı koru.")

    st.markdown("""
    <style>
    div.stButton > button {
        background: linear-gradient(145deg, #1f3a93, #2c3e50);
        color: white !important;
        height: 260px;
        width: 260px;
        font-size: 20px;
        border-radius: 20px;
        text-align: center;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border: none;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        transform: translateY(-8px) scale(1.03);
        background: linear-gradient(145deg, #34495e, #1f3a93);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }
    .center-buttons {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 3rem;
        flex-wrap: wrap;
    }
    </style>
    <div class="center-buttons">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 AI Görsel Tespiti", use_container_width=True):
            set_page("AI Görsel Tespiti")
            st.rerun()

    with col2:
        if st.button("🛡️ Poison Pill Koruma", use_container_width=True):
            set_page("Poison Pill Koruma")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 🔧 Uygulama Nasıl Çalışır?")
    st.markdown("""
        <style>
            .steps-container {
                display: flex;
                flex-wrap: wrap;
                gap: 2rem;
                margin-top: 1rem;
            }

            .step-box {
                flex: 1;
                min-width: 250px;
                padding: 1.5rem;
                border-radius: 16px;
                color: #F9FAFB;
                font-family: 'Segoe UI', sans-serif;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .step-box:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 24px rgba(0,0,0,0.4);
            }

            .step-1 { background: linear-gradient(135deg, #10B981, #059669); }
            .step-2 { background: linear-gradient(135deg, #3B82F6, #2563EB); }
            .step-3 { background: linear-gradient(135deg, #8B5CF6, #7C3AED); }

            .step-box h4 {
                margin-bottom: 0.5rem;
                font-size: 1.2rem;
                color: #FFFFFF;
            }

            .step-box p {
                margin: 0;
                font-size: 0.95rem;
                color: #E5E7EB;
            }
        </style>

        <div class='steps-container'>
            <div class='step-box step-1'>
                <h4>1. Görseli Yükle</h4>
                <p>Sosyal medyadan veya bilgisayarınızdan görselinizi yükleyin.</p>
            </div>
            <div class='step-box step-2'>
                <h4>2. AI Tespiti veya Koruma</h4>
                <p>Görselinizi analiz edin veya yapay zekaya karşı görünmez koruma uygulayın.</p>
            </div>
            <div class='step-box step-3'>
                <h4>3. Sonucu Görüntüle</h4>
                <p>Analiz sonucunu görün veya watermark'lı güvenli görseli indirin.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.stop()

# --- Eğer Seçim Yapıldıysa Devam ---

section = st.session_state.page

# Geri dönmek için Ana Sayfa butonu
if st.button("🏠 Ana Sayfaya Dön", use_container_width=True):
    st.session_state.page = None
    st.rerun()

# Sidebar Logosu ve Başlığı
st.sidebar.image("https://sdmntpritalynorth.oaiusercontent.com/files/00000000-b1e4-6246-8018-ddf632e0fe34/raw?se=2025"
                 "-04-29T23%3A27%3A55Z&sp=r&sv=2024-08-04&sr=b&scid=deff9565-83ca-5bea-a9fb-ab6285294621&skoid"
                 "=dfdaf859-26f6-4fed-affc-1befb5ac1ac2&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-29T03"
                 "%3A11%3A35Z&ske=2025-04-30T03%3A11%3A35Z&sks=b&skv=2024-08-04&sig"
                 "=kYsOgOlO2w9iwqYlDZDvZkQPNbPpdFK7bzdnuELmVJA%3D",
                 width=80)
st.sidebar.title("🏰 KaleVeri Paneli")
st.sidebar.success(f"Aktif Bölüm: {section}")


# --- Ortak Fonksiyonlar ---

def get_image_from_instagram_post(post_url):
    """Instagram postundan küçük görsel çeker"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(post_url, headers=headers)
    if response.status_code != 200:
        st.error("❌ Instagram linkinden veri çekilemedi.")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', property='og:image')
    if not meta_tag:
        st.error("❌ Fotoğraf bulunamadı!")
        return None
    image_url = meta_tag['content']
    img_response = requests.get(image_url)
    if img_response.status_code == 200:
        img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
        return img
    else:
        st.error("❌ Fotoğraf indirilemedi!")
        return None


def show_analysis(image_bytes):
    with st.spinner("🧠 Görsel analiz ediliyor..."):
        result = detect_image_ai(image_bytes)
        score_ai = result.get("prob_ai", 0.0)
        score_real = 1.0 - score_ai

    st.subheader("📊 Analiz Sonuçları")
    st.metric("🤖 AI Olasılığı", f"%{score_ai * 100:.2f}")
    st.metric("🧍 Gerçeklik Skoru", f"%{score_real * 100:.2f}")

    # Grafikler için iki sütun
    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score_ai * 100,
            title={'text': "AI Olasılığı"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#e74c3c"},
                'steps': [
                    {'range': [0, 40], 'color': "#2ecc71"},
                    {'range': [40, 70], 'color': "#f39c12"},
                    {'range': [70, 100], 'color': "#e74c3c"},
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True, key="gauge_chart")


    with col2:
        fig_pie = px.pie(
            names=["Gerçek Görsel", "AI Üretimi"],
            values=[score_real, score_ai],
            color_discrete_sequence=["#2ecc71", "#e74c3c"],
            title="🧮 Oransal Dağılım"
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")


    # Otomatik açıklama
    st.markdown("### 📌 Görsel Hakkında Değerlendirme")
    if score_ai >= 0.7:
        st.error("Bu görselin yapay zeka tarafından üretilmiş olma olasılığı yüksektir.")
    elif score_ai <= 0.3:
        st.success("Bu görsel büyük ihtimalle gerçek bir görüntüdür.")
    else:
        st.warning("Bu görselin yapay zeka ile üretilmiş olma ihtimali orta seviyededir. Daha fazla analiz önerilir.")


# --- AI Görsel Tespiti ---
if section == "AI Görsel Tespiti":
    st.header("🤖 AI İçerik Tespiti")

    tab1, tab2, tab3 = st.tabs(["🖼️   Görsel Yükle", "🌐   Instagram", "🎤   Ses Analizi"])

    with tab1:
        st.subheader("🖼️ Belgeden Görsel Yükle")
        file = st.file_uploader("Görsel seçin (PNG, JPG)", type=["png", "jpg", "jpeg"], key="image_upload")
        if file:
            image = Image.open(file).convert("RGB")
            st.image(image, caption="🖼️ Yüklenen Görsel", use_container_width=True)
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            show_analysis(buf.getvalue())

    with tab2:
        st.subheader("🌐 Instagram'dan Görsel Çek")
        post_link = st.text_input("📎 Instagram Post Linki", placeholder="https://www.instagram.com/p/...", key="insta_link")
        if post_link:
            st.markdown("## 📸 Instagram Postu")
            components.html(f"""
                <div style="display: flex; justify-content: center; align-items: center;">
                    <blockquote class="instagram-media" data-instgrm-permalink="{post_link}" data-instgrm-version="14" style="width:100%;max-width:500px;margin:20px auto;"> </blockquote>
                </div>
                <script async src="//www.instagram.com/embed.js"></script>
            """, height=650)

            st.markdown("---")
            image = get_image_from_instagram_post(post_link)
            if image:
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                show_analysis(buf.getvalue())

    with tab3:
        st.subheader("🎤 AI Ses Tespiti (İnsan mı, Yapay mı?)")
        st.info("🔈 Sadece test edilecek sesi yükleyin. Sistem içsel bir insan referans sesi kullanacaktır.")
        test_audio = st.file_uploader("🎙️ Test Edilecek Ses (WAV)", type=["wav"], key="test_audio")

        if test_audio:
            try:
                with open("gercekSes22.wav", "rb") as f:
                    ref_audio_bytes = f.read()
            except FileNotFoundError:
                st.error("❌ Referans ses dosyası bulunamadı! Lütfen proje klasörüne ekleyin.")
            else:
                with st.spinner("🧠 Ses analiz ediliyor..."):
                    result = detect_audio_ai(ref_audio_bytes, test_audio.read())

                score = result["score"]

                st.subheader("📊 Ses Analiz Sonuçları")

                if score >= 0.5:
                    st.info("✅ Bu ses büyük olasılıkla gerçek bir insana aittir.")
                else:
                    st.warning("⚠️ Bu ses büyük olasılıkla yapay (TTS/Deepfake) bir sistem tarafından üretilmiştir.")


# --- Poison Pill Koruma ---
elif section == "Poison Pill Koruma":
    st.header("🛡️ Görsel Güvenlik Araçları")

    tab1, tab2 = st.tabs(["🛡️ Poison Pill Koruma", "🔐 Görsel Kriptolama"])

    with tab1:
        file = st.file_uploader("Görsel yükle (PNG/JPG)", type=["png", "jpg", "jpeg"], key="poison_image")
        if file:
            image = Image.open(file).convert("RGB")
            st.image(image, caption="🖼️ Yüklenen Görsel", use_container_width=True)
            if st.button("🔐 Görseli Koru"):
                with st.spinner("🔧 Görsel korunuyor..."):
                    poisoned_img = poison_image(image)
                    buf = io.BytesIO()
                    poisoned_img.save(buf, format="PNG")
                st.success("✅ Görsel başarıyla korundu!")
                st.image(poisoned_img, caption="🛡️ Korumalı Görsel", use_container_width=True)
                st.download_button("⬇️ Korumalı Görseli İndir", data=buf.getvalue(), file_name="protected.png", mime="image/png")

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            carrier_file = st.file_uploader("Taşıyıcı Resim (Carrier)", type=["png", "jpg", "jpeg"], key="carrier")
            if carrier_file:
                carrier_image = Image.open(carrier_file)
                st.image(carrier_image, caption="2. Resim (Carrier)", use_container_width=True)

        with col2:
            secret_file = st.file_uploader("Gizli Resim (Secret)", type=["png", "jpg", "jpeg"], key="secret")
            if secret_file:
                secret_image = Image.open(secret_file)
                st.image(secret_image, caption="1. Resim (Secret)", use_container_width=True)

        encoded_image = None

        if st.button("🔐 Kriptola"):
            if carrier_file and secret_file:
                with st.spinner("İşleniyor..."):
                    encoded_image = encrypt_rgb_secret_into_rgb_carrier(carrier_image, secret_image)
                    st.subheader("📤 Kriptolanmış Görsel")
                    st.image(encoded_image, caption="Kriptolu Görsel", use_container_width=True)

                    buf = io.BytesIO()
                    encoded_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(label="📥 Görseli İndir",
                                       data=byte_im,
                                       file_name="encrypted_image.png",
                                       mime="image/png")
            else:
                st.warning("Lütfen iki resmi de yükleyin.")

        st.markdown("---")
        st.subheader("🔓 Gömülü Resmi Geri Çöz")

        recovery_file = st.file_uploader("📂 Kriptolu (Encoded) Görseli Yükle", type=["png", "jpg", "jpeg"], key="recover")
        if st.button("Recover Image"):
            if recovery_file:
                encoded_img = Image.open(recovery_file)
                recovered = decrypt_rgb_secret_from_carrier(encoded_img)

                st.subheader("📥 Çözülen Gizli Görsel")
                st.image(recovered, caption="Recovered Image", use_container_width=True)
            else:
                st.warning("Lütfen önce kriptolanmış bir görsel yükleyin.")
