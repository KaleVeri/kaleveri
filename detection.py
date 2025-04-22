import requests, os, json
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
    # Sonradan eklendi
    # Debug çıktısı – terminalde göreceksin
    print("📦 Gelen API verisi:\n", json.dumps(data, indent=2))

    # Hata yakalama – veri gelmezse çökmemesi için
    try:
        # prob_ai = data["media"]["ai_generated"]["score"]
        prob_ai = data["ai_generated"]["score"]

    except KeyError:
        prob_ai = 0.0
        # st.error("API'den beklenen 'media' verisi gelmedi. Yapı değişmiş olabilir.")
        st.error("API'den 'ai_generated' verisi alınamadı.")

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
