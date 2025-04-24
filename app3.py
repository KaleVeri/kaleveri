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
    "https://sdmntprwestus2.oaiusercontent.com/files/00000000-5ad4-61f8-9814-0c107c92ecaa/raw?se=2025-04-22T23%3A14%3A36Z&sp=r&sv=2024-08-04&sr=b&scid=801d565c-02b5-55a1-b5e8-6da4b4ce8c30&skoid=cdb71e28-0a5b-4faa-8cf5-de6084d65b8f&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-22T20%3A37%3A45Z&ske=2025-04-23T20%3A37%3A45Z&sks=b&skv=2024-08-04&sig=cyjsCPsbhja/WsvNLT7N7dYhdIiKebGVNtIvdnscChU%3D",
    use_container_width=True,
    caption="Kaleveri Logo"
)
st.sidebar.title("🛡️ AI Image Guard")
section = st.sidebar.radio("Fonksiyon Seçin", ["AI Görsel Tespiti", "Poison Pill Koruma"])

# Ana başlık
st.title("🎯 AI Görsel Tespiti & Koruma Platformu")
st.markdown("Yapay zeka tarafından üretilmiş görselleri analiz et, veya kendi görselini manipülasyona karşı koru.")

# Sosyal medya bağlantısı
post_link = st.text_input("📎 Sosyal Medya Post Linki", placeholder="https://instagram.com/p/...")

if post_link:
    st.markdown("#### 🔗 Sosyal Medya Bağlantısı")
    st.markdown(f"<div class='link-box'>📍 <a href='{post_link}' target='_blank'>{post_link}</a></div>", unsafe_allow_html=True)

    if "instagram.com" in post_link:
        embed_html = f"""
        <blockquote class="instagram-media" data-instgrm-permalink="{post_link}" data-instgrm-version="14" style="width:100%">
        </blockquote><script async src="//www.instagram.com/embed.js"></script>
        """
        components.html(embed_html, height=600)

    # 🔮 SAHTE ANALİZ - RASTGELE SKOR
    st.subheader("🔍 Sosyal Medya Görsel Analizi (Simülasyon)")
    score_ai = round(random.uniform(0.1, 0.9), 2)
    score_real = round(1.0 - score_ai, 2)

    col1, col2 = st.columns(2)
    col1.metric("🔵 Gerçeklik Skoru", f"{score_real*100:.2f} %")
    col2.metric("🔴 AI Skoru", f"{score_ai*100:.2f} %")

    st.markdown("<div class='score-box'>", unsafe_allow_html=True)
    st.markdown(f"""
    ✅ <b>Sonuç Özeti:</b><br/>
    <ul>
        <li><b>AI Olasılığı:</b> {score_ai*100:.2f}%</li>
        <li><b>Gerçeklik Skoru:</b> {score_real*100:.2f}%</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 🌟 Yorum
    if score_ai > 0.7:
        st.warning("⚠️ Bu görsel yüksek ihtimalle yapay zeka tarafından üretilmiş.")
    elif score_ai > 0.4:
        st.info("ℹ️ Görselde yapay zeka izi olabilir, ancak emin değiliz.")
    else:
        st.success("✅ Görsel büyük ihtimalle gerçek.")

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
        score_real = result.get("score_real", 1.0)
        score_ai = result.get("prob_ai", 0.0)

        col1, col2 = st.columns(2)
        col1.metric("🔵 Gerçeklik Skoru", f"{score_real*100:.2f} %")
        col2.metric("🔴 AI Skoru", f"{score_ai*100:.2f} %")

        st.markdown("<div class='score-box'>", unsafe_allow_html=True)
        st.markdown(f"""
        ✅ <b>Sonuç Özeti:</b><br/>
        <ul>
            <li><b>AI Olasılığı:</b> {score_ai*100:.2f}%</li>
            <li><b>Gerçeklik Skoru:</b> {score_real*100:.2f}%</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 🌟 Yorum
        if score_ai > 0.7:
            st.warning("⚠️ Bu görsel yüksek ihtimalle yapay zeka tarafından üretilmiş.")
        elif score_ai > 0.4:
            st.info("ℹ️ Görselde yapay zeka izi olabilir, ancak emin değiliz.")
        else:
            st.success("✅ Görsel büyük ihtimalle gerçek.")

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

            st.download_button(
                label="⬇️ Korumalı Görseli İndir",
                data=buf.getvalue(),
                file_name="protected.png",
                mime="image/png"
            )

        else:
            st.info("Bu işlem, Nightshade benzeri bir algoritma ile görseli AI modellerine karşı zehirler.")

            # Sosyal medya bağlantısı
            post_link = st.text_input("📎 Sosyal Medya Post Linki", placeholder="https://instagram.com/p/...")

            if post_link:
                st.markdown("#### 🔗 Sosyal Medya Bağlantısı")
                st.markdown(f"<div class='link-box'>📍 <a href='{post_link}' target='_blank'>{post_link}</a></div>",
                            unsafe_allow_html=True)

                if "instagram.com" in post_link:
                    embed_html = f"""
                    <blockquote class="instagram-media" data-instgrm-permalink="{post_link}" data-instgrm-version="14" style="width:100%">
                    </blockquote><script async src="//www.instagram.com/embed.js"></script>
                    """
                    components.html(embed_html, height=600)

                # 🔐 SAHTE KORUMA ANALİZİ - RASTGELE SKOR
                st.subheader("🧪 Sosyal Medya Üzerinden Şifreleme Tespiti (Simülasyon)")
                score_protected = round(random.uniform(0.6, 0.95), 2)
                score_vulnerable = round(1.0 - score_protected, 2)

                col1, col2 = st.columns(2)
                col1.metric("🟢 Koruma Skoru", f"{score_protected * 100:.2f} %")
                col2.metric("🔴 Zayıflık Skoru", f"{score_vulnerable * 100:.2f} %")

                st.markdown("<div class='score-box'>", unsafe_allow_html=True)
                st.markdown(f"""
                ✅ <b>Sonuç Özeti:</b><br/>
                <ul>
                    <li><b>Koruma Seviyesi:</b> {score_protected * 100:.2f}%</li>
                    <li><b>Potansiyel Zayıflık:</b> {score_vulnerable * 100:.2f}%</li>
                </ul>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # 🌟 Yorum
                if score_protected > 0.8:
                    st.success("✅ Görsel büyük ihtimalle başarıyla korunmuş.")
                elif score_protected > 0.5:
                    st.info("ℹ️ Görsel kısmen korunmuş olabilir, tam emin değiliz.")
                else:
                    st.warning("⚠️ Görselin yeterince korunmamış olma ihtimali var.")
            else:
                st.caption("👆 Eğer sosyal medya bağlantısı varsa yukarıya ekleyebilirsin.")

            if st.button("🔐 Görseli Şifrele / Zehirle"):
                with st.spinner("Görsel işleniyor…"):
                    poisoned_img = poison_image(image)
                    buf = io.BytesIO()
                    poisoned_img.save(buf, format="PNG")

                st.success("✅ Görsel şifrelendi. Aşağıdan indirebilirsiniz.")
                st.download_button(
                    "⬇️ Şifrelenmiş Görseli İndir",
                    data=buf.getvalue(),
                    file_name="protected.png",
                    mime="image/png"
                )


