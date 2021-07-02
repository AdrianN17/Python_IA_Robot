
from PIL import Image
import base64
import numpy as np
import cv2
import face_recognition

base64Data  = open("text.txt","rb").read()

jpg_original = base64.b64decode(base64Data)
jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
image_buffer = cv2.imdecode(jpg_as_np, flags=1)

face_locations = face_recognition.face_locations(image_buffer)

for face_location in face_locations:

   
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    face_image = image_buffer[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()
