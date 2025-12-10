from flask import Flask, request
import cv2
import pytesseract
import pyttsx3
import numpy as np
import time

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/upload", methods=["POST"])
def upload():
    img_bytes = request.data
    
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    filename = f"image_{int(time.time())}.jpg"
    cv2.imwrite(filename, img)
    print("Image saved:", filename)

    # OCR
    text = pytesseract.image_to_string(img)
    text = " ".join(text.split())
    print("Extracted text:", text)

    # Text to Speech
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)
    engine.say(text)
    engine.runAndWait()

    return "OK", 200

app.run(host="0.0.0.0", port=5000)
