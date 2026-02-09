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
# IMAGE TYPE DETECTION
# =========================

def detect_image_type(image: Image.Image):
    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    color_std = np.std(img)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = edges.mean()

    if color_std < 40 and edge_density > 15:
        return "handwritten"

    if color_std < 25 and edge_density > 25:
        return "sketch"

    return "jewel"

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
# LLM IMAGE DESCRIPTION
# =========================

def llm_describe_jewel(image: Image.Image) -> str:
    client = get_llm_client()
    img_b64 = image_to_base64(image)

    prompt = """
You are a jewellery expert.

Describe the jewellery in the image using:
category, material, stone type, stone shape, color.

Write one short descriptive sentence.
Do not add assumptions.
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
        max_tokens=60
    )

    return response.choices[0].message.content.strip()

# =========================
# MAIN PIPELINE
# =========================

def ocr_pipeline(image: Image.Image):
    image_type = detect_image_type(image)

    if image_type == "handwritten":
        text = llm_extract_text(image)
        return {
            "type": "handwritten",
            "text": text
        }

    description = llm_describe_jewel(image)

    return {
        "type": image_type,  # jewel or sketch
        "image": image,
        "description": description
    }
