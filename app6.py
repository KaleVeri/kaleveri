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
st.set_page_config(page_title="KaleVeri", layout="wide", page_icon="🏰")

# --- Seçim Ekranı ---
if "page" not in st.session_state:
    st.session_state.page = None


def set_page(page_name):
    st.session_state.page = page_name


if st.session_state.page is None:
    st.title("🎯 AI Görsel Tespiti & Koruma Platformu")
    st.markdown("Yapay zeka tarafından üretilmiş görselleri analiz et veya kendi görselini manipülasyona karşı koru.")
    st.markdown('<div class="center-buttons">', unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.menu-container {
        display: flex;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
        justify-content: center;
        }
        
        div.stButton > button {
            background: #f9f9f9;
            height: 260px;
            width: 260px;
            font-size: 20px;
            border-radius: 16px;
            text-align: center;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.08);
            transition: transform 0.2s;
            cursor: pointer;
            border: 2px solid transparent;
            color: black !important;
        }
        div.stButton > button:hover {
            transform: translateY(-8px);
            border: 2px solid #3498db;
        }
        .center-buttons {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 3rem;
            flex-wrap: wrap;
        }
        .back-button > button {
            background-color: #f0f0f0;
            height: 60px;
            width: 200px;
            font-size: 18px;
            border-radius: 12px;
            padding: 0.5rem 1rem;
            margin-top: 2rem;
            box-shadow: 0 6px 12px rgba(0,0,0,0.08);
            transition: transform 0.2s;
            cursor: pointer;
            border: 2px solid transparent;
            color: black !important;
        }
        .back-button > button:hover {
            transform: translateY(-4px);
            border: 2px solid #3498db;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 AI Görsel Tespiti", use_container_width=True):
            set_page("AI Görsel Tespiti")
            st.rerun()

    with col2:
        if st.button("🧪 Poison Pill Koruma", use_container_width=True):
            set_page("Poison Pill Koruma")
            st.rerun()

    # Nasıl Çalışır bölümü
    st.markdown("## 🔧 Uygulama Nasıl Çalışır?")
    st.markdown("""
        <div style='display: flex; gap: 2rem; flex-wrap: wrap;'>
            <div style='flex: 1; min-width: 250px; background: #3498db; color: white; padding: 1.5rem; border-radius: 12px;'>
                <h4>1. Görseli Yükle</h4>
                <p>Sosyal medyadan veya bilgisayarınızdan görselinizi yükleyin.</p>
            </div>
            <div style='flex: 1; min-width: 250px; background: #e67e22; color: white; padding: 1.5rem; border-radius: 12px;'>
                <h4>2. AI Tespiti veya Koruma</h4>
                <p>Görselinizi analiz edin veya yapay zekaya karşı koruyun.</p>
            </div>
            <div style='flex: 1; min-width: 250px; background: #2ecc71; color: white; padding: 1.5rem; border-radius: 12px;'>
                <h4>3. Sonucu Görüntüle</h4>
                <p>Yüzde olarak analiz sonucunu görün veya korunan görseli indirin.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# Eğer kartlardan birine tıkladıysan artık normal işlemler:
section = st.session_state.page

# Sayfalara Ana Sayfaya Dön butonu
if section in ["AI Görsel Tespiti", "Poison Pill Koruma"]:
    if st.button("🏠 Ana Sayfaya Dön", use_container_width=True):
        st.session_state.page = None
        st.rerun()

# Sidebar
st.sidebar.image(
    "https://sdmntpritalynorth.oaiusercontent.com/files/00000000-b1e4-6246-8018-ddf632e0fe34/raw?se=2025-04-28T22"
    "%3A37%3A13Z&sp=r&sv=2024-08-04&sr=b&scid=e69a32eb-1ee9-546b-a1bf-19b6fba9e978&skoid=06e05d6f-bdd9-4a88-a7ec"
    "-2c0a779a08ca&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-28T05%3A55%3A43Z&ske=2025-04-29T05%3A55"
    "%3A43Z&sks=b&skv=2024-08-04&sig=G2Tdzp15rguoF0ASXSme2284wtGck9%2BPqxweqtFPHI8%3D",
    width=60
)
st.sidebar.title(" KaleVeri")
st.sidebar.success(f"Aktif Fonksiyon: {section}")


def show_score_summary(label_1, score_1, label_2, score_2):
    st.markdown(f""" <div style='display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;'> <div 
    style='background: #e74c3c; padding: 1rem 1.5rem; border-radius: 12px; color: white; flex: 1; min-width: 200px; 
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);'> <h4 style='margin: 0;'>{label_1}</h4>
            <h2 style='margin: 0;'>{score_1 * 100:.2f} %</h2> </div> <div style='background: #27ae60; padding: 1rem 
            1.5rem; border-radius: 12px; color: white; flex: 1; min-width: 200px; box-shadow: 0 4px 8px rgba(0,0,0,
            0.05);'> <h4 style='margin: 0;'>{label_2}</h4>
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
        text=[f"{score_ai * 100:.1f}%", f"{(1 - score_ai) * 100:.1f}%"],
        textposition='auto'
    ))
    fig3.update_layout(title="🔎 AI vs Gerçeklik Skoru", xaxis=dict(range=[0, 1]))
    st.plotly_chart(fig3, use_container_width=True)


# --- Grafik Fonksiyonları Sonu ---

# Sosyal medya gösterimi
def show_social_post(link):
    st.markdown("#### 🔗 Sosyal Medya Postu")
    icon = "📷" if "instagram" in link else "🔗"
    st.markdown(f"""
        <div style='background: #f0f0f0; padding: 1rem; border-left: 5px solid #3498db; border-radius: 8px; margin-bottom: 1rem;'>
            <b>{icon}</b> <a href=\"{link}\" target=\"_blank\">{link}</a>
        </div>
    """, unsafe_allow_html=True)

    if "instagram.com" in link:
        embed_html = f"""
        <blockquote class=\"instagram-media\" data-instgrm-permalink=\"{link}\" data-instgrm-version=\"14\" style=\"width:100%\"> </blockquote><script async src=\"//www.instagram.com/embed.js\"></script>"""
        components.html(embed_html, height=600)


# --- Simülasyon bölümü (Güncellendi) ---
if section == "AI Görsel Tespiti":
    post_link = st.text_input("📎 Sosyal Medya Post Linki", placeholder="https://instagram.com/p/... ")
    if post_link:
        show_social_post(post_link)
        st.subheader("🔍 AI Görsel Tespiti (Simülasyon)")
        score_ai = round(random.uniform(0.1, 0.9), 2)
        score_real = 1 - score_ai
        show_score_summary("AI Olasılığı", score_ai, "Gerçeklik Skoru", score_real)
        interpret_score(score_ai, "detection")
        show_graphic_show(score_ai, score_real)

# 📤 Görsel Yükleme
st.markdown("## 📤 Görsel Yükleme")
file = st.file_uploader("📷 Görsel yükleyin (PNG/JPG)", type=["png", "jpg", "jpeg"])

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
            st.download_button("⬇️ Korumalı Görseli İndir", data=buf.getvalue(), file_name="protected.png",
                               mime="image/png")
