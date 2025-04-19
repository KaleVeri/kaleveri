import numpy as np
from PIL import Image
import subprocess, tempfile, os, io

# Seçenek 1 – resmi local Nightshade CLI’ye göndermek
def poison_image(img: Image.Image) -> Image.Image:
    """
    Eğer Nightshade CLI kurulmuşsa onu çalıştır,
    yoksa hızlı bir 'spektral jitter + yüksek‑freq. gürültü' fallback uygula.
    """
    try:
        bin_path = os.getenv("NIGHTSHADE_BIN", "/usr/local/bin/nightshade")
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp_in, \
             tempfile.NamedTemporaryFile(suffix=".png") as tmp_out:
            img.save(tmp_in.name)
            subprocess.run([bin_path, "--input", tmp_in.name,
                                       "--output", tmp_out.name,
                                       "--strength", "0.25"],
                           check=True)
            return Image.open(tmp_out.name)
    except Exception:
        # Fallback – küçük, insan‑gözünün algılayamayacağı Gauss gürültüsü
        arr = np.asarray(img).astype(np.float32)
        noise = np.random.normal(0, 2.5, arr.shape)
        poisoned = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(poisoned)
