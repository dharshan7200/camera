from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import cv2
import numpy as np
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOBILE_STREAM_URL = "http://100.125.160.56:8080/shot.jpg"

class CaptureRequest(BaseModel):
    lat: float
    lon: float
    time: str

@app.post("/capture")
def capture(data: CaptureRequest):

    try:
        # 📸 Get snapshot
        response = requests.get(MOBILE_STREAM_URL, timeout=5)

        if response.status_code != 200:
            return {"status": "error", "message": "Camera not reachable"}

        img_arr = np.frombuffer(response.content, np.uint8)
        frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return {"status": "error", "message": "Image decode failed"}

        # 🖊️ Overlay ONLY location + time
# 🖊️ Format time only
# 🖊️ Format time
# 🖊️ Format time
        formatted_time = datetime.fromisoformat(data.time.replace("Z","")).strftime("%d-%m-%Y %H:%M:%S")

        # 🖊️ Location text
        location_text = f"Lat:{data.lat:.4f} Lon:{data.lon:.4f}"

        # Background box (increase height)
        cv2.rectangle(
            frame,
            (0, frame.shape[0]-70),
            (frame.shape[1], frame.shape[0]),
            (0,0,0),
            -1
        )

        # Line 1 → Time
        cv2.putText(
            frame,
            formatted_time,
            (10, frame.shape[0]-40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )

        # Line 2 → Location
        cv2.putText(
            frame,
            location_text,
            (10, frame.shape[0]-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )
        # 💾 Save image
        filename = f"capture_{int(datetime.now().timestamp())}.jpg"
        cv2.imwrite(filename, frame)

        return {"status": "SAFE", "file": filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}