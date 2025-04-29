"""
FastAPI sunucusu
--------------------------------------------
• POST /api/detection   : Son AI-tespiti verisini kaydeder
• GET  /api/detection   : En son AI-tespiti verisini döndürür
• POST /api/protection  : Son koruma verisini kaydeder
• GET  /api/protection  : En son koruma verisini döndürür
• GET  /health          : Yaşıyor mu?  (200 OK)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn

app = FastAPI(title="AI-Demo Backend")

# Bellekte “son gelen” verileri tutuyoruz (demo amaçlı)
STATE: Dict[str, Optional[dict]] = {"detection": None, "protection": None}

# ---------- Şema tanımları ----------
class DetectionIn(BaseModel):
    image_b64: str                 # Yüklenen resim (Base64)
    probability: float             # 0-1
    model_scores: Dict[str, float] # {"GPT-4o": 0.73, ...}

class ProtectionIn(BaseModel):
    encrypted_b64: str             # Şifrelenmiş resim
    manipulations_b64: List[str]   # <= 3 adet

# ---------- Endpoint’ler ------------
@app.post("/api/detection", status_code=204)
def post_detection(item: DetectionIn):
    STATE["detection"] = item.dict()

@app.get("/api/detection")
def get_detection():
    if STATE["detection"] is None:
        raise HTTPException(404, "No data yet")
    return STATE["detection"]

@app.post("/api/protection", status_code=204)
def post_protection(item: ProtectionIn):
    STATE["protection"] = item.dict()

@app.get("/api/protection")
def get_protection():
    if STATE["protection"] is None:
        raise HTTPException(404, "No data yet")
    return STATE["protection"]

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- Çalıştır ---------------
if __name__ == "__main__":
    uvicorn.run("live_api:app", host="0.0.0.0", port=7010, reload=False)
