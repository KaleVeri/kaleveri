import streamlit as st
from PIL import Image
import numpy as np
import cv2
import io


def encrypt_rgb_secret_into_rgb_carrier(carrier, secret):
    carrier = np.array(carrier.convert('RGB'))
    secret = np.array(secret.convert('RGB'))

    secret = cv2.resize(secret, (carrier.shape[1], carrier.shape[0]))
    carrier_encoded = carrier.copy()

    for c in range(3):
        secret_4bit = (secret[:, :, c] >> 4)
        carrier_encoded[:, :, c] = (carrier_encoded[:, :, c] & 0b11110000) | secret_4bit

    return Image.fromarray(carrier_encoded)


def decrypt_rgb_secret_from_carrier(encoded):
    encoded = np.array(encoded.convert('RGB'))
    recovered = np.zeros_like(encoded)

    for c in range(3):
        extracted = encoded[:, :, c] & 0b00001111
        recovered[:, :, c] = extracted << 4

    return Image.fromarray(recovered.astype(np.uint8))


st.title("🧠 Görsel Kriptolama Arayüzü")

col1, col2 = st.columns(2)

with col1:
    carrier_file = st.file_uploader("Taşıyıcı Resim (Carrier)", type=["png", "jpg", "jpeg"])
    if carrier_file:
        carrier_image = Image.open(carrier_file)
        st.image(carrier_image, caption="2. Resim (Carrier)", use_container_width=True)

with col2:
    secret_file = st.file_uploader("Gizli Resim (Secret)", type=["png", "jpg", "jpeg"])
    if secret_file:
        secret_image = Image.open(secret_file)
        st.image(secret_image, caption="1. Resim (Secret)", use_container_width=True)

encoded_image = None

if st.button("🔐 Kriptola"):
    if carrier_file and secret_file:
        with st.spinner("İşleniyor..."):
            encoded_image = encrypt_rgb_secret_into_rgb_carrier(carrier_image, secret_image)

            st.subheader("📤 Kriptolanmış Görsel")
            st.image(encoded_image, caption="Kriptolu Görsel", use_container_width=True)

            # İndirme butonu
            buf = io.BytesIO()
            encoded_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(label="📥 Kriptolu Görseli İndir",
                               data=byte_im,
                               file_name="encrypted_image.png",
                               mime="image/png")
    else:
        st.warning("Lütfen iki resmi de yükleyin.")

# Recovery alanı
st.markdown("---")
st.subheader("🔓 Gömülü Resmi Geri Çöz")

recovery_file = st.file_uploader("📂 Kriptolu (Encoded) Görseli Yükle", type=["png", "jpg", "jpeg"])
if st.button("Recover Image"):
    if recovery_file:
        encoded_img = Image.open(recovery_file)
        recovered = decrypt_rgb_secret_from_carrier(encoded_img)

        st.subheader("📥 Çözülen Gizli Görsel")
        st.image(recovered, caption="Recovered Image", use_container_width=True)
    else:
        st.warning("Lütfen önce kriptolanmış bir görsel yükleyin.")
