# detection_audio.py

import tempfile
import numpy as np
import soundfile as sf
from resemblyzer import VoiceEncoder, preprocess_wav
import streamlit as st

# Modeli bir kez indirip cache’e alıyoruz
encoder = VoiceEncoder()

def detect_audio_ai(ref_bytes: bytes, test_bytes: bytes) -> dict:
    """
    - ref_bytes: Gerçek insan sesi örneği (baytlar)
    - test_bytes: Şüpheli ses dosyası (baytlar)
    """
    # 1) Referans sesi geçici dosyaya yaz, embed çıkar
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_ref:
        tmp_ref.write(ref_bytes)
        tmp_ref.flush()
        ref_wav = preprocess_wav(tmp_ref.name)  # artık tek değer
    ref_emb = encoder.embed_utterance(ref_wav)

    # 2) Test sesini aynı şekilde işle
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_test:
        tmp_test.write(test_bytes)
        tmp_test.flush()
        test_wav = preprocess_wav(tmp_test.name)
    test_emb = encoder.embed_utterance(test_wav)

    # 3) Kosinüs benzerliği
    sim = float(
        np.dot(ref_emb, test_emb)
        / (np.linalg.norm(ref_emb) * np.linalg.norm(test_emb))
    )

    # 4) Eşikle sınıflandırma
    label = "human" if sim > 0.75 else "synthetic"

    return {
        "label": label,
        "score": sim,
        "raw":   {"cosine_similarity": sim},
    }

