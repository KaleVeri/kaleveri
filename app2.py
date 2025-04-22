import streamlit as st
from PIL import Image
import io
from detection import detect_image_ai, plot_detection_result
from nightshade_wrap import poison_image

# Sayfa başı ayarı – EN ÜSTE KOYULMALI!
st.set_page_config(page_title="AI Image Guard", layout="wide", page_icon="🛡️")

# Özelleştirilmiş CSS – Arkaplan rengi, yazı tipi, kenarlık vb.
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
    .css-1aumxhk {
        background-color: #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://sdmntprwestus2.oaiusercontent.com/files/00000000-5ad4-61f8-9814-0c107c92ecaa/raw?se=2025-04-22T21%3A51%3A48Z&sp=r&sv=2024-08-04&sr=b&scid=c827048e-3d33-50a0-8dbd-477034afb72f&skoid=cdb71e28-0a5b-4faa-8cf5-de6084d65b8f&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-22T20%3A35%3A00Z&ske=2025-04-23T20%3A35%3A00Z&sks=b&skv=2024-08-04&sig=7lb%2BLLXt9GuwG2YG1tGBkNe0hbIfDaN7etxp8aX182o%3D", use_container_width=True, caption="Kaleveri Logo")  # logoyu değiştir
st.sidebar.title("🛡️ AI Image Guard")
section = st.sidebar.radio("Fonksiyon Seçin", ["AI Görsel Tespiti", "Poison Pill Koruma"])

# Ana Başlık
st.title("🎯 AI Görsel Tespiti & Koruma Platformu")
st.markdown("Yapay zeka tarafından üretilmiş görselleri analiz et, veya kendi görselini manipülasyona karşı koru.")

# Fake sosyal medya link input (fake alan!)
social_link = st.text_input("📎 Sosyal Medya Post Linki (isteğe bağlı)", placeholder="https://instagram.com/p/...")

# Görsel Yükleme
file = st.file_uploader("📷 Görsel yükleyin (PNG/JPG)", type=["png", "jpg", "jpeg"])
post_link = st.text_input("Sosyal medya postu linki", placeholder="https://instagram.com/... veya https://twitter.com/...")
if post_link:
    st.caption(f"🔗 Bağlantı: {post_link}")

if file:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="Yüklenen Görsel", use_container_width=True)

    if section == "AI Görsel Tespiti":
        with st.spinner("🧠 Görsel analiz ediliyor…"):
            result = detect_image_ai(file.getvalue())

        st.subheader("🔎 Tespit Sonuçları")
        st.metric("AI Üretim Olasılığı", f"{result['prob_ai']:.1%}")
        st.json(result["summary"])     # özet skorları göster
        plot_detection_result(result)  # grafik

    else:
        st.info("Bu işlem, Nightshade benzeri bir algoritma ile görseli AI modellerine karşı zehirler.")
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
