"""
LLM-based OCR + Image Understanding pipeline
Detects: jewel image / sketch / handwritten
Uses vision-capable LLM instead of TrOCR
"""

import os
import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# =========================
# CONFIG (ENV BASED)
# =========================

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_VISION_MODEL = os.getenv("LLM_MODEL")

def get_llm_client():
    return OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL
    )


# =========================
# IMAGE → BASE64
# =========================

def image_to_base64(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# =========================
# LLM HANDWRITTEN TEXT EXTRACTION
# =========================

def llm_extract_text(image: Image.Image) -> str:
    client = get_llm_client()
    img_b64 = image_to_base64(image)

    prompt = """
You are a handwriting transcription assistant.

Read the handwritten text in the image.
Fix spelling mistakes.
Return only the extracted text.
Do not explain anything.
if no text is found just return "image"
"""

    response = client.chat.completions.create(
        model=LLM_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.0,
        max_tokens=50
    )

    return response.choices[0].message.content.strip()


# =========================
# MAIN PIPELINE
# =========================

def ocr_pipeline(image: Image.Image):
    image_type = llm_extract_text(image)

    if image_type != "image":
        return {
            "type": "handwritten",
            "text": image_type
        }


    return {
        "type": "image",
        "image": image
    }
