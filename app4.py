import streamlit as st
from PIL import Image
import io
import random
from detection import detect_image_ai, plot_detection_result
from nightshade_wrap import poison_image
import streamlit.components.v1 as components

# Sayfa ayarı
st.set_page_config(page_title="AI Image Guard", layout="wide", page_icon="🛡️")

# Genel CSS
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    a {
        text-decoration: none;
        color: #3498db;
    }
    .link-box {
        background-color: #ecf0f1;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 5px solid #3498db;
    }
    .score-box {
        background-color: #f7f7f7;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image(
    "https://sdmntprwestus2.oaiusercontent.com/files/00000000-5ad4-61f8-9814-0c107c92ecaa/raw?se=2025-04-24T17%3A34"
    "%3A04Z&sp=r&sv=2024-08-04&sr=b&scid=205e5ec4-232a-503e-a4ef-47f3c9bd0184&skoid=ae70be19-8043-4428-a990"
    "-27c58b478304&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-24T03%3A28%3A37Z&ske=2025-04-25T03%3A28"
    "%3A37Z&sks=b&skv=2024-08-04&sig=rrCKHlBiq6H/IAZr0MCEH3QBjxMg7T4N5FDTgIynVqU%3D",
    use_container_width=True,
    caption="Kaleveri Logo"
)
st.sidebar.title("🛡️ AI Image Guard")
section = st.sidebar.radio("Fonksiyon Seçin", ["AI Görsel Tespiti", "Poison Pill Koruma"])

# Ana başlık
st.title("🎯 AI Görsel Tespiti & Koruma Platformu")
st.markdown("Yapay zeka tarafından üretilmiş görselleri analiz et veya kendi görselini manipülasyona karşı koru.")


# Ortak fonksiyonlar
def show_social_post(link):
    st.markdown("#### 🔗 Sosyal Medya Bağlantısı")
    st.markdown(f"<div class='link-box'>📍 <a href='{link}' target='_blank'>{link}</a></div>", unsafe_allow_html=True)
    if "instagram.com" in link:
        embed_html = f"""
        <blockquote class="instagram-media" data-instgrm-permalink="{link}" data-instgrm-version="14" 
        style="width:100%"> </blockquote><script async src="//www.instagram.com/embed.js"></script>"""
        components.html(embed_html, height=600)


def show_score_card(title1, value1, title2, value2):
    col1, col2 = st.columns(2)
    col1.metric(title1, f"{value1 * 100:.2f} %")
    col2.metric(title2, f"{value2 * 100:.2f} %")


def show_score_summary(label_1, score_1, label_2, score_2):
    st.markdown("<div class='score-box'>", unsafe_allow_html=True)
    st.markdown(f"""
    ✅ <b>Sonuç Özeti:</b><br/>
    <ul>
        <li><b>{label_1}:</b> {score_1 * 100:.2f}%</li>
        <li><b>{label_2}:</b> {score_2 * 100:.2f}%</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def interpret_score(score, mode):
    if mode == "detection":
        if score > 0.7:
            st.warning("⚠️ Bu görsel yüksek ihtimalle yapay zeka tarafından üretilmiş.")
        elif score > 0.4:
            st.info("ℹ️ Görselde yapay zeka izi olabilir, ancak emin değiliz.")
        else:
            st.success("✅ Görsel büyük ihtimalle gerçek.")
    elif mode == "protection":
        if score > 0.8:
            st.success("✅ Görsel büyük ihtimalle başarıyla korunmuş.")
        elif score > 0.5:
            st.info("ℹ️ Görsel kısmen korunmuş olabilir, tam emin değiliz.")
        else:
            st.warning("⚠️ Görselin yeterince korunmamış olma ihtimali var.")


# Sosyal medya bağlantısı
post_link = st.text_input("📎 Sosyal Medya Post Linki", placeholder="https://instagram.com/p/...")
if post_link:
    show_social_post(post_link)

    # 🔮 SAHTE ANALİZ
    if section == "AI Görsel Tespiti":
        st.subheader("🔍 Sosyal Medya Görsel Analizi (Simülasyon)")
        score_ai = round(random.uniform(0.1, 0.9), 2)
        score_real = 1.0 - score_ai
        show_score_card("🔵 Gerçeklik Skoru", score_real, "🔴 AI Skoru", score_ai)
        show_score_summary("AI Olasılığı", score_ai, "Gerçeklik Skoru", score_real)
        interpret_score(score_ai, "detection")

    elif section == "Poison Pill Koruma":
        st.subheader("🧪 Sosyal Medya Üzerinden Şifreleme Tespiti (Simülasyon)")
        score_protected = round(random.uniform(0.6, 0.95), 2)
        score_vulnerable = 1.0 - score_protected
        show_score_card("🟢 Koruma Skoru", score_protected, "🔴 Zayıflık Skoru", score_vulnerable)
        show_score_summary("Koruma Seviyesi", score_protected, "Potansiyel Zayıflık", score_vulnerable)
        interpret_score(score_protected, "protection")
else:
    st.caption("👆 Eğer sosyal medya bağlantısı varsa yukarıya ekleyebilirsin.")

# Görsel yükleme
file = st.file_uploader("📷 Görsel yükleyin (PNG/JPG)", type=["png", "jpg", "jpeg"])
if file:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="🖼️ Yüklenen Görsel", use_container_width=True)

    if section == "AI Görsel Tespiti":
        with st.spinner("🧠 Görsel analiz ediliyor…"):
            result = detect_image_ai(file.getvalue())
        st.subheader("🔎 Tespit Sonuçları")
        score_ai = result.get("prob_ai", 0.0)
        score_real = result.get("score_real", 1.0)
        show_score_card("🔵 Gerçeklik Skoru", score_real, "🔴 AI Skoru", score_ai)
        show_score_summary("AI Olasılığı", score_ai, "Gerçeklik Skoru", score_real)
        interpret_score(score_ai, "detection")
        st.json(result.get("summary", {}))
        plot_detection_result(result)

    elif section == "Poison Pill Koruma":
        st.info("🔐 Bu işlem, Nightshade benzeri bir algoritma ile görseli AI modellerine karşı korur.")
        if st.button("🛡️ Görseli Koru / Zehirle"):
            with st.spinner("Görsel korunuyor…"):
                poisoned_img = poison_image(image)
                buf = io.BytesIO()
                poisoned_img.save(buf, format="PNG")

            st.success("✅ Görsel başarıyla korundu!")
            st.image(poisoned_img, caption="🛡️ Korumalı Görsel", use_container_width=True)
            st.download_button("⬇️ Korumalı Görseli İndir", data=buf.getvalue(), file_name="protected.png",
                               mime="image/png")
