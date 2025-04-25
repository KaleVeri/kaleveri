import streamlit as st
from PIL import Image
import io
import random
from detection import detect_image_ai
from nightshade_wrap import poison_image
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px

# Sayfa Ayarı
st.set_page_config(page_title="AI Image Guard", layout="wide", page_icon="🛡️")

# CSS (Yükleme kutusu dahil)
st.markdown("""
    <style>
    .custom-upload-wrapper {
        position: relative;
        border: 2px dashed #2980b9;
        border-radius: 12px;
        background-color: #ecf7fc;
        padding: 2.5rem 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .custom-upload-wrapper p {
        margin: 0;
        font-weight: bold;
        color: #2980b9;
        font-size: 1.1rem;
    }
    .custom-upload-wrapper small {
        display: block;
        color: #2980b9;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }
    .custom-upload-btn-container {
        position: absolute;
        bottom: 1rem;
        right: 1rem;
    }
    .custom-upload-btn {
        background-color: #2980b9;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 500;
        text-decoration: none;
    }
    input[type="file"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emojione_1F6E1.svg/2048px-Emojione_1F6E1.svg.png", width=60)
st.sidebar.title("🛡️ AI Image Guard")
section = st.sidebar.radio("Fonksiyon Seçin", ["AI Görsel Tespiti", "Poison Pill Koruma"])

# Başlık
st.title("🎯 AI Görsel Tespiti & Koruma Platformu")
st.markdown("Yapay zeka tarafından üretilmiş görselleri analiz et veya kendi görselini manipülasyona karşı koru.")

# Sosyal medya gösterimi
def show_social_post(link):
    st.markdown("#### 🔗 Sosyal Medya Postu")
    icon = "📷" if "instagram" in link else "🔗"
    st.markdown(f"""
        <div style='
            background: #f0f0f0;
            padding: 1rem;
            border-left: 5px solid #3498db;
            border-radius: 8px;
            margin-bottom: 1rem;
        '>
            <b>{icon}</b> <a href="{link}" target="_blank">{link}</a>
        </div>
    """, unsafe_allow_html=True)

    if "instagram.com" in link:
        embed_html = f"""
        <blockquote class="instagram-media" data-instgrm-permalink="{link}" data-instgrm-version="14" 
        style="width:100%"> </blockquote><script async src="//www.instagram.com/embed.js"></script>"""
        components.html(embed_html, height=600)

# Skor kutuları
def show_score_summary(label_1, score_1, label_2, score_2):
    st.markdown(f"""
    <div style='
        display: flex; 
        gap: 1rem; 
        margin-top: 1rem;
        flex-wrap: wrap;
    '>
        <div style='
            background: #e74c3c; 
            padding: 1rem 1.5rem; 
            border-radius: 12px; 
            color: white; 
            flex: 1;
            min-width: 200px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        '>
            <h4 style='margin: 0;'>{label_1}</h4>
            <h2 style='margin: 0;'>{score_1 * 100:.2f} %</h2>
        </div>
        <div style='
            background: #27ae60; 
            padding: 1rem 1.5rem; 
            border-radius: 12px; 
            color: white;
            flex: 1;
            min-width: 200px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        '>
            <h4 style='margin: 0;'>{label_2}</h4>
            <h2 style='margin: 0;'>{score_2 * 100:.2f} %</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

def interpret_score(score, mode):
    if mode == "detection":
        if score > 0.7:
            st.warning("⚠️ Bu görsel yüksek ihtimalle yapay zeka tarafından üretilmiş.")
        elif score > 0.4:
            st.info("ℹ️ Görselde yapay zeka izi olabilir.")
        else:
            st.success("✅ Görsel büyük ihtimalle gerçek.")
    elif mode == "protection":
        if score > 0.8:
            st.success("✅ Görsel büyük ihtimalle başarıyla korunmuş.")
        elif score > 0.5:
            st.info("ℹ️ Görsel kısmen korunmuş olabilir.")
        else:
            st.warning("⚠️ Görsel yeterince korunmamış olabilir.")

def show_graphic_show(score_ai, score_real):
    st.subheader("🎨 Grafiksel Görsel Analiz")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 🎯 AI Olasılığı Göstergesi")
        fig1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score_ai * 100,
            title={'text': "AI Olasılığı"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#e74c3c"},
                'steps': [
                    {'range': [0, 40], 'color': "#2ecc71"},
                    {'range': [40, 70], 'color': "#f39c12"},
                    {'range': [70, 100], 'color': "#e74c3c"}
                ]
            }
        ))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("##### 🧠 Oransal Dağılım")
        fig2 = px.pie(
            names=["AI", "Gerçek"],
            values=[score_ai, 1 - score_ai],
            color=["AI", "Gerçek"],
            color_discrete_map={"AI": "#e74c3c", "Gerçek": "#27ae60"},
            hole=0.3
        )
        fig2.update_traces(textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("##### 📊 Yatay Karşılaştırma")
    fig3 = go.Figure(go.Bar(
        x=[score_ai, 1 - score_ai],
        y=["AI", "Gerçek"],
        orientation='h',
        marker=dict(color=['#e74c3c', '#27ae60']),
        text=[f"{score_ai*100:.1f}%", f"{(1-score_ai)*100:.1f}%"],
        textposition='auto'
    ))
    fig3.update_layout(title="🔎 AI vs Gerçeklik Skoru", xaxis=dict(range=[0, 1]))
    st.plotly_chart(fig3, use_container_width=True)

# Sosyal medya
post_link = st.text_input("📎 Sosyal Medya Post Linki", placeholder="https://instagram.com/p/...")
if post_link:
    show_social_post(post_link)
    if section == "AI Görsel Tespiti":
        st.subheader("🔍 AI Görsel Tespiti (Simülasyon)")
        score_ai = round(random.uniform(0.1, 0.9), 2)
        score_real = 1 - score_ai
        show_score_summary("AI Olasılığı", score_ai, "Gerçeklik Skoru", score_real)
        interpret_score(score_ai, "detection")
        show_graphic_show(score_ai, score_real)
    elif section == "Poison Pill Koruma":
        st.subheader("🧪 Koruma Tespiti (Simülasyon)")
        score_protect = round(random.uniform(0.6, 0.95), 2)
        score_vuln = 1 - score_protect
        show_score_summary("Koruma Skoru", score_protect, "Zayıflık Skoru", score_vuln)
        interpret_score(score_protect, "protection")

# 📤 Görsel Yükleme Kutusu (tek kutu - çalışır Browse files)
st.markdown("## 📤 Görsel Yükleme")
st.markdown("""
    <div class="custom-upload-wrapper">
        <p>Dosyanızı buraya sürükleyin veya yüklemek için göz atın.</p>
        <small>Limit 200MB per file • PNG, JPG, JPEG</small>
        <div class="custom-upload-btn-container">
            <label for="file-upload" class="custom-upload-btn">Browse files</label>
        </div>
    </div>
""", unsafe_allow_html=True)
file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="file-upload", label_visibility="collapsed")

# Görsel işle
if file:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="🖼️ Yüklenen Görsel", use_container_width=True)

    if section == "AI Görsel Tespiti":
        with st.spinner("🧠 Görsel analiz ediliyor..."):
            result = detect_image_ai(file.getvalue())

        st.subheader("📊 Analiz Sonuçları")
        score_ai = result.get("prob_ai", 0.0)
        score_real = 1.0 - score_ai
        show_score_summary("AI Olasılığı", score_ai, "Gerçeklik Skoru", score_real)
        interpret_score(score_ai, "detection")
        st.json(result.get("summary", {}))
        show_graphic_show(score_ai, score_real)

    elif section == "Poison Pill Koruma":
        st.info("🧬 Görsel, yapay zeka modellerine karşı korumalı hale getirilecektir.")
        if st.button("🛡️ Görseli Koru"):
            with st.spinner("🔧 Görsel korunuyor..."):
                poisoned_img = poison_image(image)
                buf = io.BytesIO()
                poisoned_img.save(buf, format="PNG")
            st.success("✅ Görsel başarıyla korundu!")
            st.image(poisoned_img, caption="🛡️ Korumalı Görsel", use_container_width=True)
            st.download_button("⬇️ Korumalı Görseli İndir", data=buf.getvalue(), file_name="protected.png", mime="image/png")