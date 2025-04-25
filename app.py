"""
#  app.py
import io

import streamlit as st
from PIL import Image

from detection import detect_image_ai, plot_detection_result
from nightshade_wrap import poison_image

st.set_page_config(page_title="AI Image Guard", layout="wide")
st.sidebar.title("🛡️ AI Image Guard")
section = st.sidebar.radio("Fonksiyon Seçin", ["AI Görsel Tespiti", "Poison Pill Koruma"])

file = st.file_uploader("Fotoğraf yükleyin (PNG/JPG)", type=["png", "jpg", "jpeg"])

if file:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="Yüklenen Görsel", use_column_width=True)

    if section == "AI Görsel Tespiti":
        with st.spinner("Görsel analiz ediliyor…"):
            result = detect_image_ai(file.getvalue())
        st.subheader("🔎 Sonuç")
        st.json(result["summary"])          # ham skorları göster
        plot_detection_result(result)       # bar/line chart
        # ek güven skor metrikleri
        st.metric("AI Üretim Olasılığı", f"{result['prob_ai']:.1%}")

    else:  # Poison Pill
        st.info("Bu işlem, Nightshade benzeri bir algoritma kullanarak görseli AI modellerine karşı zehirler.")
        if st.button("Görseli Şifrele / Zehirle"):
            poisoned_img = poison_image(image)
            buf = io.BytesIO()
            poisoned_img.save(buf, format="PNG")
            st.success("Görsel şifrelendi. 👇 İndirebilirsiniz.")
            st.download_button(
                "Şifrelenmiş Görseli İndir",
                data=buf.getvalue(),
                file_name="protected.png",
                mime="image/png"
            )
"""

# app.py
import io

import streamlit as st
from PIL import Image

from detection import detect_image_ai, plot_detection_result
from nightshade_wrap import poison_image

# Sayfa ayarları
st.set_page_config(page_title="AI Image Guard", layout="wide", page_icon="🛡️")

# Kenar çubuğu
st.sidebar.title("🛡️ AI Image Guard")
section = st.sidebar.radio("Fonksiyon Seçin", ["AI Görsel Tespiti", "Poison Pill Koruma"])

st.title("🎯 AI Görsel Tespiti & Koruma Platformu")
st.markdown("Yapay zekâ tarafından üretilmiş görselleri tespit et ve raporla.")

# Dosya yükleme
file = st.file_uploader("📷 Görsel yükleyin (PNG/JPG)", type=["png", "jpg", "jpeg"])

if file:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="Yüklenen Görsel", use_column_width=True)

    if section == "AI Görsel Tespiti":
        with st.spinner("🧠 Görsel analiz ediliyor…"):
            result = detect_image_ai(img_bytes=file.getvalue())

        # Ana sonuç başlığı
        st.subheader("🔎 Tespit Sonuçları")

        # 1️⃣ Float değerleri al
        ai_p   = result["prob_ai"]    # örn. 0.83
        real_p = result["prob_real"]  # örn. 0.17

        # 2️⃣ Yüzdeleri yan yana göster
        c1, c2 = st.columns(2)
        c1.metric("Gerçeklik Skoru", f"{real_p:.2%}")
        c2.metric("AI Skoru",        f"{ai_p:.2%}")

        # 3️⃣ Opsiyonel: JSON özetini genişletilebilir şekilde göster
        with st.expander("📄 Özet JSON"):
            st.json(result["summary"])

        # 4️⃣ Bar grafiği
        plot_detection_result(result)

    else:
        st.info("📦 Bu işlem, Nightshade tarzı ‘poison pill’ ile görseli AI modellerine karşı zehirler.")
        if st.button("🔐 Görseli Şifrele / Zehirle"):
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
