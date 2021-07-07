import base64
import numpy as np
import cv2
import face_recognition
import json


from PyQt5 import QtGui

import time

from PIL import Image, ImageDraw
from PyQt5.QtGui import QTextCursor

from Models.data_decision import data_decision
from Models.data_robot import data_robot
from Models.detalle_fabrica import detalle_fabrica
from Models.fsm_decision import fsm_decision


class ia:

    def __init__(self, img, txt):
        self.img = img
        self.txt = txt

        json_face_data_string = open('face_data.json', )
        self.json_face_data = json.load(json_face_data_string)

        json_decision_data_string = open('decision_data.json')
        self.json_decision_data = json.load(json_decision_data_string)

        self.rostrosBD =[]
        self.nombresBD = []
        self.decisionBD = []


        for data in self.json_face_data:

            face = face_recognition.load_image_file(data["img"])
            encoding = face_recognition.face_encodings(face)[0]
            self.rostrosBD.append(encoding)
            self.nombresBD.append(data["nombre"])


        for data in self.json_decision_data:
            objDecision = detalle_fabrica()
            objDecision.nombre = data["nombre"]
            objDecision.porcentaje = data["porcentaje"]
            objDecision.porcentaje_real = objDecision.porcentaje
            objDecision.prioridad = data["prioridad"]
            objDecision.tiempo_desgaste = data["tiempo_desgaste"]

            self.decisionBD.append(objDecision)

        self.decision = data_decision()


        self.fsm = fsm_decision()

    def clear_decision(self):
        self.decision.accion = ""
        self.decision.cantidad_caras = 0

    def get_datajson(self):
        self.decision.accion = self.fsm.state
        return json.dumps(self.decision.__dict__)

    def read_json(self, json_data):

       if json_data != "":
            self.clear_decision()

            data_parse = json.loads(json_data)

            tipo = data_parse["tipo"]

            if tipo == "robotData":

                self.aplicar_recfacial(data_parse["data"])

            elif tipo == "objetivo":
                self.aplicar_reabastecimiento(data_parse["objetivo"])

    def aplicar_recfacial(self, imgb64):
        jpg_original = base64.b64decode(imgb64)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        image_buffer = cv2.imdecode(jpg_as_np, flags=1)

        face_locations = face_recognition.face_locations(image_buffer)
        face_encodings = face_recognition.face_encodings(image_buffer, face_locations)

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

            texto = "{} Una cara ha sido reconocida Top: {}, Left: {}, Bottom: {}, Right: {} \n".format(
                time.strftime("%H:%M:%S"), top, left, bottom, right)
            self.txt.insertPlainText(texto)
            self.txt.moveCursor(QTextCursor.End)

            self.decision.cantidad_caras += 1


        del draw

        open_cv_image = np.array(pil_image)

        img = QtGui.QImage(open_cv_image.data, open_cv_image.shape[1], open_cv_image.shape[0],
                           QtGui.QImage.Format_RGB888).rgbSwapped()

        pixmap = QtGui.QPixmap.fromImage(img)

        self.img.setPixmap(pixmap)

    def aplicar_tiempo(self):

        listado_pesos = []

        for data in self.decisionBD:
            data.porcentaje_real -= data.tiempo_desgaste

            texto = "{} Materia prima consumida de fabrica {}, Porcentaje {}\n".format(
                time.strftime("%H:%M:%S"), data.nombre, data.porcentaje_real)
            self.txt.insertPlainText(texto)

            listado_pesos.append(self.calcular_disminucion(data))

        index = listado_pesos.index(min(listado_pesos))

        self.elegir_direccion(index)

    def elegir_direccion(self, i):

        if self.fsm.state == "abastecido":

            if i == 0:
                self.fsm.irA()
            elif i == 1:
                self.fsm.irB()
            elif i == 2:
                self.fsm.irC()

    def resetear_decision(self):

        self.fsm.reseteo_fsm()

        for data in self.decisionBD:
            data.porcentaje_real = data.porcentaje

    @staticmethod
    def calcular_disminucion(data):
        return data.porcentaje_real - (data.prioridad * data.tiempo_desgaste)

    def aplicar_reabastecimiento(self, objetivo):
        if(objetivo == "A"):
            self.fsm.irNoAbastecido()
            self.decisionBD[0].porcentaje_real = 100
            self.txt.insertPlainText("Punto A abastecido : \n")

        elif (objetivo == "B"):
            self.fsm.irNoAbastecido()
            self.decisionBD[1].porcentaje_real = 100
            self.txt.insertPlainText("Punto B abastecido : \n")

        elif (objetivo == "C"):
            self.fsm.irNoAbastecido()
            self.decisionBD[2].porcentaje_real = 100
            self.txt.insertPlainText("Punto C abastecido : \n")

        elif (objetivo == "R"):
            self.fsm.irAbastecido()
            self.txt.insertPlainText("Robot abastecido : \n")


