from PIL import Image
import numpy as np
import cv2

def encrypt_rgb_secret_into_rgb_carrier(carrier_image: Image.Image, secret_image: Image.Image) -> Image.Image:
    """
    RGB bir gizli resmi, RGB taşıyıcıya 4-bit olarak gömer.
    """
    carrier = np.array(carrier_image.convert('RGB'))
    secret = np.array(secret_image.convert('RGB'))

    # Gizli resmi taşıyıcının boyutuna göre yeniden boyutlandır
    secret = cv2.resize(secret, (carrier.shape[1], carrier.shape[0]))

    carrier_encoded = carrier.copy()

    # Her kanal için 4 bit şifreleme
    for c in range(3):  # RGB kanalları
        secret_4bit = (secret[:, :, c] >> 4)  # Üst 4 bit alınır
        carrier_encoded[:, :, c] = (carrier_encoded[:, :, c] & 0b11110000) | secret_4bit

    return Image.fromarray(carrier_encoded)


def decrypt_rgb_secret_from_carrier(encoded_image: Image.Image) -> Image.Image:
    """
    Şifrelenmiş RGB taşıyıcıdan, 4-bit çözülmüş gizli resmi çıkarır.
    """
    encoded = np.array(encoded_image.convert('RGB'))
    recovered = np.zeros_like(encoded)

    for c in range(3):
        extracted = encoded[:, :, c] & 0b00001111  # Alt 4 bit çıkarılır
        recovered[:, :, c] = extracted << 4        # Üste taşınarak kaliteye yakın görüntü elde edilir

    return Image.fromarray(recovered.astype(np.uint8))
