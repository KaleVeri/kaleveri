import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests, base64, io, numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import qrcode

BACKEND = "http://localhost:7010"
REFRESH_MS = 3000

# ---------------- Yardımcılar -----------------
def b64_to_img(b64: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")

def make_qr(url: str):
    return qrcode.make(url).convert("RGB")

def gauge(prob: float):
    fig, ax = plt.subplots(figsize=(3,1.8), subplot_kw={"projection":"polar"})
    ax.bar(np.linspace(-np.pi/2, np.pi/2, 100), 1,
           width=np.pi/100, bottom=0, color="#eeeeee")
    ax.bar(np.linspace(-np.pi/2, -np.pi/2 + prob*np.pi, 100), 1,
           width=np.pi/100, bottom=0, color="#e63946")
    ax.set_axis_off(); ax.set_ylim(0,1)
    return fig

# ------------- Sayfa Ayarları & Refresh ------------
st.set_page_config(page_title="AI Detection & Protection", layout="wide")
st_autorefresh(interval=REFRESH_MS, key="data_refresh")

LEFT, RIGHT = st.columns(2, gap="large")

# ---------------- SOL BLOK — AI Tespiti -------------
with LEFT:
    st.markdown("## 🕵️‍♂️ AI Tespiti")
    qr_det = make_qr(f"{BACKEND}/api/detection")
    c1, c2, c3 = st.columns([1,0.2,1])
    c1.image(qr_det, caption="Kodu Okutun", use_container_width=True)
    c2.markdown("<h2 style='text-align:center;margin-top:65px'>➡️</h2>",
                unsafe_allow_html=True)

    try:
        det = requests.get(f"{BACKEND}/api/detection", timeout=1).json()
        img_det = b64_to_img(det["image_b64"])
        c3.image(img_det, caption="Yüklenen Resim", use_container_width=True)

        st.markdown("---")
        st.pyplot(gauge(det["probability"]), clear_figure=True)
        st.markdown(f"### **%{det['probability']*100:.0f} Veri AI ile Üretilmiş!**")

        st.markdown("##### AI Olasılığı (Model Bazlı):")
        fig, ax = plt.subplots(figsize=(3,2))
        ax.barh(list(det["model_scores"].keys()),
                list(det["model_scores"].values()))
        ax.set_xlim(0,1); ax.set_xlabel("Olasılık"); plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    except Exception:
        c3.image(
            np.full((250,250,3), 240, dtype=np.uint8),
            caption="Henüz veri yok", use_container_width=True
        )
        st.info("API /api/detection tetiklendiğinde sonuçlar görünecek.")

# -------------- SAĞ BLOK — AI Koruması ---------------
with RIGHT:
    st.markdown("## 🛡️ AI Koruması")
    qr_prot = make_qr(f"{BACKEND}/api/protection")
    d1, d2, d3 = st.columns([1,0.2,1])
    d1.image(qr_prot, caption="Kodu Okutun", use_container_width=True)
    d2.markdown("<h2 style='text-align:center;margin-top:65px'>➡️</h2>",
                unsafe_allow_html=True)

    try:
        prot = requests.get(f"{BACKEND}/api/protection", timeout=1).json()
        enc_img = b64_to_img(prot["encrypted_b64"])
        d3.image(enc_img, caption="Şifrelenmiş Resim", use_container_width=True)

        st.markdown("#### Şifrelenmiş Veri Testi:")
        st.caption("prompt: Görseli Netleştir")

        cols = st.columns(3)
        for c, b64 in zip(cols, prot["manipulations_b64"][:3]):
            c.image(b64_to_img(b64), use_container_width =True)
    except Exception:
        d3.image(
            np.full((250,250,3), 240, dtype=np.uint8),
            caption="Henüz veri yok", use_container_width=True
        )
        st.info("API /api/protection tetiklendiğinde sonuçlar görünecek.")

# ------------------------- Footer --------------------
st.markdown("""
<hr style="margin-top:40px;">
<div style="text-align:center;font-size:0.9rem;color:gray">
© 2025 KaleVeri AI Detection & Protection Demo
</div>
""", unsafe_allow_html=True)
