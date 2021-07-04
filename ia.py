import base64
import numpy as np
import cv2
import face_recognition
import json


from PyQt5 import QtGui

import time

from PIL import Image, ImageDraw

from Models.data_decision import data_decision
from Models.data_robot import data_robot


class ia:

    def __init__(self, img, txt):
        self.obj = data_robot()
        self.img = img
        self.txt = txt

        json_array_string = open('face_data.json', )
        self.json_array_img = json.load(json_array_string)

        self.rostrosBD =[]
        self.nombresBD = []


        for data in self.json_array_img:

            face = face_recognition.load_image_file(data["img"])
            encoding = face_recognition.face_encodings(face)[0]
            self.rostrosBD.append(encoding)
            self.nombresBD.append(data["nombre"])



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

            self.obj.tipo = data_parse["tipo"]

            if self.obj.tipo == "robotData":

                self.obj.accion = data_parse["accion"]
                self.obj.data = data_parse["data"]
                self.obj.objetivo = data_parse["objetivo"]

                self.aplicar_recfacial(self.obj.data)

            elif self.obj.tipo == "reabastecido":
                pass





    def aplicar_recfacial(self, imgb64):
        jpg_original = base64.b64decode(imgb64)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        image_buffer = cv2.imdecode(jpg_as_np, flags=1)

        face_locations = face_recognition.face_locations(image_buffer)
        face_encodings = face_recognition.face_encodings(image_buffer, face_locations)

        pil_image = Image.fromarray(jpg_as_np)
        draw = ImageDraw.Draw(pil_image)

        pil_image = Image.fromarray(image_buffer)
        draw = ImageDraw.Draw(pil_image)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.rostrosBD, face_encoding)

            name = "Desconocido"

            face_distances = face_recognition.face_distance(self.rostrosBD, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.nombresBD[best_match_index]

            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


        del draw

        open_cv_image = np.array(pil_image)

        img = QtGui.QImage(open_cv_image.data, open_cv_image.shape[1], open_cv_image.shape[0],
                           QtGui.QImage.Format_RGB888).rgbSwapped()

        pixmap = QtGui.QPixmap.fromImage(img)

        self.img.setPixmap(pixmap)


