import base64
import numpy as np
import cv2
import face_recognition
import json


from PyQt5 import QtGui

import time

from Models.data_decision import data_decision
from Models.data_robot import data_robot


class ia:

    def __init__(self, img, txt):
        self.obj = data_robot()
        self.img = img
        self.txt = txt

        json_array_string = open('face_data.json', )
        self.json_array_img = json.load(json_array_string)

        #print(self.json_array_img[0]["nombre"])

        self.decision = data_decision()

    def clear_decision(self):
        self.decision.accion = ""
        self.decision.cantidad_caras = 0

    def get_datajson(self):
        return json.dumps(self.decision.__dict__)

    def read_json(self, json_data):

       if json_data != "":
            self.clear_decision()

            data_parse = json.loads(json_data)

            self.obj.accion = data_parse["accion"]
            self.obj.data = data_parse["data"]
            self.obj.objetivo = data_parse["objetivo"]

            self.aplicar_recfacial(self.obj.data)





    def aplicar_recfacial(self, imgb64):
        jpg_original = base64.b64decode(imgb64)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        image_buffer = cv2.imdecode(jpg_as_np, flags=1)

        face_locations = face_recognition.face_locations(image_buffer)


        for face_location in face_locations:
            top, right, bottom, left = face_location

            texto = "{} Una cara ha sido reconocida Top: {}, Left: {}, Bottom: {}, Right: {} \n".format(time.strftime("%H:%M:%S"),top, left, bottom,right)


            self.txt.insertPlainText(texto)

            self.decision.cantidad_caras+= 1

            #face_image = image_buffer[top:bottom, left:right]

            #print(texto)

        img = QtGui.QImage(image_buffer.data, image_buffer.shape[1], image_buffer.shape[0],
                           QtGui.QImage.Format_RGB888).rgbSwapped()

        pixmap = QtGui.QPixmap.fromImage(img)

        self.img.setPixmap(pixmap)


