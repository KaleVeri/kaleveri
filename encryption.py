import torch
import clip
import numpy as np
from PIL import Image

# Cihaz ayari
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

def clip_defend(pil_image):
    """
    Bir PIL Image'ı CLIP tabanlı küçük bir adversarial saldırıyla korur.
    """
    # Preprocess
    image_input = clip_preprocess(pil_image).unsqueeze(0).to(device)
    image_input.requires_grad = True

    # Yanıltıcı hedef prompt
    text_inputs = torch.cat([clip.tokenize("a blurry abstract painting")]).to(device)

    # Saldırı parametreleri
    alpha = 1/255
    iterations = 10

    # CLIP adversarial saldırı
    for _ in range(iterations):
        image_input.requires_grad = True
        logits_per_image, _ = clip_model(image_input, text_inputs)
        loss = -logits_per_image[0][0]
        clip_model.zero_grad()
        loss.backward()
        grad = image_input.grad.sign()
        image_input = image_input + alpha * grad
        image_input = torch.clamp(image_input, 0, 1).detach()

    # Tensoru PIL Image'a donustur
    adv_image_np = image_input.squeeze(0).detach().cpu().numpy()
    adv_image_np = np.transpose(adv_image_np, (1, 2, 0)) * 255
    adv_image_np = adv_image_np.clip(0, 255).astype(np.uint8)
    defended_image = Image.fromarray(adv_image_np)

    return defended_image
