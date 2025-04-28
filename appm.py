# app.py
import io
import streamlit as st
from PIL import Image

from detection import detect_image_ai, plot_detection_result
from detection_audio import detect_audio_ai
from nightshade_wrap import poison_image

# ——— Sayfa Ayarları ———
st.set_page_config(
    page_title="AI Guard",
    page_icon="🛡️",
    layout="wide"
)

# ——— Mod Seçimi ———
mode = st.sidebar.radio(
    "🚦 Mod Seçin",
    ["AI Görsel Tespiti", "AI Ses Tespiti", "Poison Pill Koruma"]
)

st.title("🎯 AI Guard Platformu")

# ——— AI Görsel Tespiti ———
if mode == "AI Görsel Tespiti":
    st.header("📷 AI Görsel Tespiti")
    img_file = st.file_uploader("Görsel yükleyin (PNG/JPG)", type=["png","jpg","jpeg"])
    if img_file:
        image = Image.open(img_file).convert("RGB")
        st.image(image, caption="Yüklenen Görsel", use_column_width=True)

        with st.spinner("🧠 Görsel analiz ediliyor…"):
            res = detect_image_ai(img_file.getvalue())

        # AI vs Real
        c1, c2 = st.columns(2)
        c1.metric("🤖 AI Olasılığı",    f"{res['prob_ai']:.2%}")
        c2.metric("🧑‍🤝‍🧑 Gerçeklik Skoru", f"{res['prob_real']:.2%}")

        # Basit bar grafiği
        st.markdown("---")
        plot_detection_result(res)

        # Ham JSON (detaylı teknik inceleme)
        with st.expander("📂 Ham API Cevabı"):
            st.json(res["raw"])


# ——— AI Ses Tespiti ———
elif mode == "AI Ses Tespiti":
    st.header("🎙️ AI Ses Tespiti")

    # 1) Referans & Test dosyaları
    ref_file  = st.file_uploader("➡️ Referans (gerçek insan sesi)", type=["wav","mp3"])
    test_file = st.file_uploader("🎧 Test edilecek ses dosyası",  type=["wav","mp3"])
    if not ref_file or not test_file:
        st.info("Her iki dosyayı da yüklemeniz gerekiyor.")
        st.stop()

    # 2) Sesleri Dinle (Expander)
    with st.expander("🔊 Sesleri Dinle"):
        st.markdown("**Referans Ses:**"); st.audio(ref_file)
        st.markdown("**Test Ses:**");      st.audio(test_file)

    # 3) Analiz
    with st.spinner("🧠 Ses analiz ediliyor…"):
        result = detect_audio_ai(
            ref_bytes = ref_file.getvalue(),
            test_bytes= test_file.getvalue(),
        )

    # 4) Skor & Etiket
    sim   = result["score"]          # 0–1
    diff  = 1 - sim
    label = result["label"]          # "human" veya "synthetic"
    pct   = f"{sim:.1%}"

    # Alert olarak ana sonucu göster
    if label == "human":
        st.success(f"✅ Bu sesin gerçek bir insana ait olma olasılığı: {pct}")
    else:
        st.error(  f"⚠️ Bu sesin yapay (TTS/deepfake) olma olasılığı: {pct}")

    # 5) İki büyük kart: Benzerlik & Farklılık
    c1, c2 = st.columns(2)
    c1.metric("🔍 Benzerlik", pct)
    c2.metric("📉 Farklılık", f"{diff:.1%}")

    # 6) Ham Çıktı (teknik detayı görmek isteyenler)
    with st.expander("📂 Modelin Döndürdüğü Detaylı Veriler"):
        st.markdown(
            "_Not: Burası teknik inceleme içindir._"
        )
        raw = result["raw"]
        st.write({
            "cosine_similarity": raw.get("cosine_similarity"),
            "threshold_used":    0.75,
            "final_label":       label
        })
        # Diğer ham veriler
        extras = {k: raw[k] for k in raw if k not in ["cosine_similarity"]}
        if extras:
            st.markdown("**Diğer Ham Alanlar**")
            st.json(extras)


# ——— Poison Pill Koruma ———
else:
    st.header("🛡️ Poison Pill Koruma")
    img_file = st.file_uploader("Görsel yükleyin (PNG/JPG)", type=["png","jpg","jpeg"])
    if img_file:
        image = Image.open(img_file).convert("RGB")
        st.image(image, caption="Yüklenen Görsel", use_column_width=True)

        if st.button("🔐 Görseli Koru"):
            with st.spinner("🔧 Görsel korunuyor…"):
                poisoned = poison_image(image)
                buf = io.BytesIO()
                poisoned.save(buf, format="PNG")
            st.success("✅ Görsel başarıyla korundu!")
            st.image(poisoned, caption="🛡️ Korumalı Görsel", use_column_width=True)
            st.download_button(
                "⬇️ Korumalı Görseli İndir",
                data=buf.getvalue(),
                file_name="protected.png",
                mime="image/png"
            )

