
# app.py
import io
import streamlit as st
from PIL import Image

from detection import detect_image_ai, plot_detection_result
from detection_audio import detect_audio_ai
from nightshade_wrap import poison_image

# ——— Sayfa Ayarları ———
st.set_page_config(page_title="AI Guard", page_icon="🛡️", layout="wide")

# ——— Session State Başlat ———
if "ref_bytes" not in st.session_state:
    st.session_state.ref_bytes = None

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

        c1, c2 = st.columns(2)
        c1.metric("🤖 AI Olasılığı",    f"{res['prob_ai']:.2%}")
        c2.metric("🧑‍🤝‍🧑 Gerçeklik Skoru", f"{res['prob_real']:.2%}")

        st.markdown("---")
        plot_detection_result(res)

        with st.expander("📂 Ham API Cevabı"):
            st.json(res["raw"])


# ——— AI Ses Tespiti ———
elif mode == "AI Ses Tespiti":
    st.header("🎙️ AI Ses Tespiti")

    # 1) Eğer referans yoksa yalnızca referans uploader göster
    if not st.session_state.ref_bytes:
        ref_file = st.file_uploader(
            "➡️ Referans (tek seferlik, gerçek insan sesi)",
            type=["wav","mp3"],
            key="ref"
        )
        if ref_file:
            st.session_state.ref_bytes = ref_file.getvalue()
            st.success("✅ Referans sesi kaydedildi! Artık test dosyası yükleyebilirsiniz.")
        st.stop()

    # 2) Referans varsa, sadece test dosyasını sor
    test_file = st.file_uploader(
        "🎧 Test edilecek ses dosyası",
        type=["wav","mp3"],
        key="test"
    )
    if not test_file:
        st.info("Lütfen test ses dosyasını yükleyin.")
        st.stop()

    # 3) Dinleme bölümü
    with st.expander("🔊 Sesleri Dinle"):
        st.markdown("**Referans Ses (insan):**")
        st.audio(st.session_state.ref_bytes, format="audio/wav")
        st.markdown("**Test Ses:**")
        st.audio(test_file, format="audio/wav")

    # 4) Analiz
    with st.spinner("🧠 Ses analiz ediliyor…"):
        result = detect_audio_ai(
            ref_bytes = st.session_state.ref_bytes,
            test_bytes= test_file.getvalue(),
        )

    sim   = result["score"]          # 0–1
    diff  = 1 - sim
    label = result["label"]          # "human" veya "synthetic"
    pct   = f"{sim:.1%}"

    # 5) Ana Sonuç
    if label == "human":
        st.success(f"✅ Gerçek insan sesi olma olasılığı: {pct}")
    else:
        st.error(f"⚠️ Yapay (TTS/deepfake) ses olma olasılığı: {pct}")

    # 6) Kartlar
    c1, c2 = st.columns(2)
    c1.metric("🔍 Benzerlik", pct)
    c2.metric("📉 Farklılık", f"{diff:.1%}")

    # 7) Detaylı Ham Çıktı
    with st.expander("🔧 Modelin Döndürdüğü Detaylı Veriler"):
        st.markdown(
            "_Not: Bu bölüm teknik amaçlıdır. Normal kullanıcılar için özet ekran yeterlidir._"
        )
        raw = result["raw"]
        summary = {
            "cosine_similarity": raw.get("cosine_similarity"),
            "threshold_used":    0.75,
            "final_label":       label
        }
        st.write(summary)
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

