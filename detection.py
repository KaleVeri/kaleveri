"""import requests, os, json
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO


def detect_image_ai(img_bytes: bytes) -> dict:
    cfg = st.secrets["ai_detection"]
    resp = requests.post(
        cfg["endpoint"],
        data={
            "models": cfg["models"],
            "api_user": cfg["API_USER"],
            "api_secret": cfg["API_SECRET"]
        },
        files={"media": ("image.jpg", img_bytes)}
    )
    data = resp.json()
    # Sightengine sonucundan özetlik çıkar
    # Sonradan eklendi(serra)
    # Debug çıktısı – terminalde göreceksin
    print("📦 Gelen API verisi:\n", json.dumps(data, indent=2))

    # Hata yakalama – veri gelmezse çökmemesi için
    try:
        # prob_ai = data["media"]["ai_generated"]["score"] eski hali
        prob_ai = data["ai_generated"]["score"]#(serra)

    except KeyError:
        prob_ai = 0.0
        # st.error("API'den beklenen 'media' verisi gelmedi. Yapı değişmiş olabilir.") eski hali
        st.error("API'den 'ai_generated' verisi alınamadı.") #serra's version

    # buraya kadar
    return {
        "raw": data,
        "prob_ai": prob_ai,
        "summary": {
            "Gerçeklik Skoru": f"{1 - prob_ai:.2%}",
            "AI Olasılığı": f"{prob_ai:.2%}"
        }
    }


def plot_detection_result(res: dict):
    fig, ax = plt.subplots()
    ax.bar(["Real", "AI"], [1 - res["prob_ai"], res["prob_ai"]])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Olasılık")
    st.pyplot(fig)
"""

"""
detection.py
AI-üretimi görsel tespiti  –  Sightengine ‘genai’ modeli
"""

import json
import requests
import matplotlib.pyplot as plt
import streamlit as st


API_TIMEOUT = 15  # saniye – istek kilitlenmesin diye


# ----------------------------------------------------------------------
# Ana fonksiyon
# ----------------------------------------------------------------------
def detect_image_ai(img_bytes: bytes) -> dict:
    """
    Yüklenen görseli Sightengine 'genai' modeli ile analiz eder.
    Dönen sözlük:
        {
          "prob_ai": 0.83,
          "summary": {...},
          "raw": {...}
        }
    """
    cfg = st.secrets["ai_detection"]  # .streamlit/secrets.toml

    with st.spinner('Görsel analiz ediliyor...'):
        try:
            resp = requests.post(
                cfg.get("endpoint", "https://api.sightengine.com/1.0/check.json"),
                data={
                    "models": cfg.get("models", "genai"),
                    "api_user": cfg["API_USER"],
                    "api_secret": cfg["API_SECRET"],
                },
                files={"media": ("upload.jpg", img_bytes, "image/jpeg")},
                timeout=API_TIMEOUT,
            )
        except requests.exceptions.RequestException as e:
            st.error(f"API isteği sırasında hata oluştu: {e}")
            st.stop()

    if resp.status_code != 200:
        st.error(f"API isteği başarısız! (Durum Kodu: {resp.status_code})")
        st.stop()

    # Yanıtı JSON’a çevir & debug logu
    try:
        data = resp.json()
    except ValueError:
        st.error("API yanıtı JSON formatında değil!")
        st.stop()

    # Ham veri terminal çıktısı
    print("📦 Gelen API verisi:\n", json.dumps(data, indent=2))

    # Skoru çıkart
    try:
        prob_ai = float(data["type"]["ai_generated"])
    except (KeyError, TypeError, ValueError):
        prob_ai = 0.0
        st.error("API yanıtında 'type.ai_generated' alanı bulunamadı!")
        st.stop()

    st.success("Görsel başarıyla analiz edildi.")

    return {
        "raw": data,
        "prob_ai": prob_ai,
        "summary": {
            "Gerçeklik Skoru": f"{1 - prob_ai:.2%}",
            "AI Olasılığı": f"{prob_ai:.2%}"
        }
    }

# ----------------------------------------------------------------------
# Basit bar grafiği
# ----------------------------------------------------------------------
def plot_detection_result(res: dict) -> None:
    prob_ai = res["prob_ai"]
    fig, ax = plt.subplots()
    ax.bar(["Gerçek", "AI"], [1 - prob_ai, prob_ai])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Olasılık")
    ax.set_title("Görsel Gerçeklik Analizi")
    st.pyplot(fig)