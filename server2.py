from flask import Flask, request
import cv2
import pytesseract
import pyttsx3
import numpy as np
import os
import time
import threading

app = Flask(__name__)

# Create folder to save images
SAVE_FOLDER = "images"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Initialize pyttsx3 engine once globally
engine = pyttsx3.init()
engine.setProperty('rate', 120)

def process_image(img, filename):
    # Save image
    cv2.imwrite(filename, img)
    print("Image saved:", filename)

    # OCR
    text = pytesseract.image_to_string(img)
    text = " ".join(text.split())
    print("Extracted text:", text)

    # Text-to-Speech
    engine.say(text)
    engine.runAndWait()

@app.route("/upload", methods=["POST"])
def upload():
    img_bytes = request.data
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    filename = os.path.join(SAVE_FOLDER, f"image_{int(time.time())}.jpg")

    # Use a thread to avoid blocking the server
    threading.Thread(target=process_image, args=(img, filename)).start()

    return "OK", 200

if __name__ == "__main__":
    # Run on all network interfaces
    app.run(host="0.0.0.0", port=5000)
