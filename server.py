import socket
import json

continueLoop = True

BUFFER_SIZE = 1024
TCP_IP = "127.0.0.1"
TCP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
sock.bind((TCP_IP, TCP_PORT))

sock.listen(1)

connection, client_address = sock.accept()

jsonObjStr = ""

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

while continueLoop:

    data = connection.recv(BUFFER_SIZE)

    if data: 
        jsonObjStr += str(data, 'utf-8') 

        if validateJSON(jsonObjStr):
            print('received')
            jsonObjStr = ""

        


connection.close()
socket.close()



    

    
    
    