import socket
import json
from threading import *

BUFFER_SIZE = 1024
TCP_IP = "127.0.0.1"
TCP_PORT = 5005

class server():

    def __init__(self, ia_obj):
        self.jsonObjStr = ""
        self.t1 = None
        self.stop_threads = False

        self.ia = ia_obj

    @staticmethod
    def validate_json(data):
        try:
            json.loads(data)
        except ValueError as err:
            return False
        return True

    def create_thread(self):
        if not self.t1:
            self.stop_threads = False
            self.t1 = Thread(target=self.handle_client)

            self.t1.start()

    def get_json(self):
        return self.jsonObjStr

    def delete_thread(self):
        if self.t1:
            self.stop_threads = True
            self.t1.join()
            self.t1 = None


    def handle_client(self):

        try:
            self.sock = socket.socket(socket.AF_INET,  # Internet
                                      socket.SOCK_STREAM)  # TCP
            self.sock.bind((TCP_IP, TCP_PORT))

            self.jsonObjStr = ""

            self.sock.listen(1)

            connection, client_address = self.sock.accept()

            while True:

                if self.stop_threads:
                    connection.close()
                    break

                data = connection.recv(BUFFER_SIZE)

                if data:
                    str_data = str(data, 'utf-8')
                    self.jsonObjStr += str_data

                    if self.validate_json(self.jsonObjStr):
                        print("aceptado")
                        self.ia.read_json(self.jsonObjStr)
                        self.jsonObjStr = ""
                        connection.send(str.encode(self.ia.get_datajson()))
        finally:
            self.sock.close()








