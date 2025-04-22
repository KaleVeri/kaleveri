# app.py
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
