import pytesseract
import cv2
from PIL import Image
import os
import pyttsx3

language = 'en'

webcam = cv2.VideoCapture(0)
while True:
    try:
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('z'):
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()

            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

            string = pytesseract.image_to_string('saved_img.jpg')
            print(string)

            cleaned = " ".join(string.split())   # Clean text

            engine = pyttsx3.init()
            engine.setProperty('rate', 125)

            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)

            engine.say("Reading the extracted text.")
            engine.say(cleaned)

            print("Speaking...")
            engine.runAndWait()      # <-- Makes script wait until speech completes

            print("Speech complete.")
            input("Press ENTER to exit...")

            cv2.destroyAllWindows()
            break

    except KeyboardInterrupt:
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
