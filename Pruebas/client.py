import socket

TCP_IPC = "127.0.0.1"
TCP_PORTC = 5006


TCP_IP = "127.0.0.1"
TCP_PORT = 5005
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % TCP_IP)
print("UDP target port: %s" % TCP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP

sock.bind((TCP_IPC, TCP_PORTC))

sock.connect((TCP_IP,TCP_PORT));

sock.send(MESSAGE)

while True:

    

    data = sock.recvfrom(16) # buffer size is 1024 bytes
    
    if data:
        print('received {!r}'.format(data))
        sock.send(MESSAGE)

socket.close()