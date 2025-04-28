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
   
    cfg = st.secrets["ai_detection"]         # .streamlit/secrets.toml

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

    # ---------------------------------
    # Yanıtı JSON’a çevir & debug logu
    # ---------------------------------
    try:
        data = resp.json()
    except ValueError:
        st.error("API yanıtı JSON formatında değil!")
        return {"raw": {}, "prob_ai": 0.0, "summary": {}}

    # Terminalde (veya Streamlit server log’unda) ham çıktıyı gör
    print("📦 Gelen API verisi:\n", json.dumps(data, indent=2))

    # ---------------------------------
    # Skoru çıkart
    # ---------------------------------
    try:
        # Sightengine formatı:  data["type"]["ai_generated"]  → 0-1 float
        prob_ai = float(data["type"]["ai_generated"])
    except (KeyError, TypeError, ValueError):
        prob_ai = 0.0
        st.error("API yanıtında 'type.ai_generated' alanı bulunamadı!")

    return {
        "raw": data,
        "prob_ai": prob_ai,
         "prob_real": 1.0 - prob_ai,  # 0–1 arası float
        "summary": {
            "Gerçeklik Skoru": f"{1 - prob_ai:.2%}",
            "AI Olasılığı":   f"{prob_ai:.2%}",
        },
    }


# ----------------------------------------------------------------------
# Basit bar grafiği
# ----------------------------------------------------------------------
def plot_detection_result(res: dict) -> None:
    prob_ai = res["prob_ai"]
    fig, ax = plt.subplots()
    ax.bar(["Gerçek", "AI"], [res["prob_real"], res["prob_ai"]])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Olasılık")
    st.pyplot(fig)
"""


# detection.py

# detection.py
import json
import requests
import matplotlib.pyplot as plt
import streamlit as st

API_TIMEOUT = 15  # saniye

def detect_image_ai(img_bytes: bytes) -> dict:
    cfg = st.secrets["ai_detection"]
    resp = requests.post(
        cfg["endpoint"],
        data={
            "models":   cfg["models"],
            "api_user": cfg["API_USER"],
            "api_secret": cfg["API_SECRET"],
        },
        files={"media": ("upload.jpg", img_bytes, "image/jpeg")},
        timeout=API_TIMEOUT,
    )
    data = resp.json()
    # — debug
    print("📦 Gelen API verisi:\n", json.dumps(data, indent=2))

    # AI <-> Real
    ai_score   = float(data["type"]["ai_generated"])
    real_score = 1.0 - ai_score

    # Photo vs Illustration
    photo_score        = data["type"].get("photo", 0.0)
    illustration_score = data["type"].get("illustration", 0.0)

    # Quality
    quality_obj   = data.get("quality", {})
    quality_score = quality_obj.get("score", 0.0)

    # Properties
    sharpness  = data.get("sharpness", 0.0)
    brightness = data.get("brightness", 0.0)
    contrast   = data.get("contrast", 0.0)
    colors     = data.get("colors", {}).get("dominant", {}).get("hex", "#000000")

    # Deepfake
    deepfake_score = data.get("deepfake", {}).get("score", 0.0)

    return {
        "raw":                data,
        "prob_ai":            ai_score,
        "prob_real":          real_score,
        "photo_score":        photo_score,
        "illustration_score": illustration_score,
        "quality_score":      quality_score,
        "sharpness":          sharpness,
        "brightness":         brightness,
        "contrast":           contrast,
        "dominant_color":     colors,
        "deepfake_score":     deepfake_score,
    }

def plot_detection_result(res: dict) -> None:
    """
    Basit bar grafiği: Real vs AI
    """
    fig, ax = plt.subplots()
    ax.bar(["Real", "AI"], [res["prob_real"], res["prob_ai"]])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Olasılık")
    st.pyplot(fig)
