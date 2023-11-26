
# this mocks the "client" that sends the request with pico as the "server"


import socket
import time

# pico_w_host = '192.168.4.1'
host = '192.168.4.1'
port = 80

# uncomment flags to send different messages
#FLAG = "forward"
FLAG = "off"


if FLAG == "forward":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'motor forward')
        data = s.recv(1024)

    print(f'received {data!r}')


if FLAG == "backwards":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'motor backwards')
        data = s.recv(1024)

    print(f'received {data!r}')


if FLAG == "off":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'motor off')
        data = s.recv(1024)

    print(f'received {data!r}')



