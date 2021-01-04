import socket
import errno, time
import os
import sys

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1233
gameover = 0
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

print('OK')

while True:

    Response = ClientSocket.recv(2048)
    clientType = Response.decode('utf-8')
    if clientType == '1':
        while True:
            Input = input('Cuvantul pentru Spanzuratoare: ')
            time.sleep(0.5)
            ClientSocket.send(str.encode(Input))
            time.sleep(0.5)
            Input = input('Descriere: ')
            time.sleep(0.5)
            ClientSocket.send(str.encode(Input))
            time.sleep(0.5)
            # Play again
            msg = ClientSocket.recv(2048).decode('utf-8')
            if msg == '\nS-a deconectat jucatorul':
                print(msg)
                print("\nEXITING")
                ClientSocket.close()
                sys.exit()
            print(msg)

    if clientType == '2':

        print('Loading . . .')
        while True:
            msg = ClientSocket.recv(2048).decode('utf-8')
            if msg == '\nWaiting for a word and description . . . ':
                time.sleep(1)
                print(msg)
                print(ClientSocket.recv(2048).decode('utf-8'))
            else:
                print(ClientSocket.recv(2048).decode('utf-8'))

            InputLetter = input(ClientSocket.recv(2048).decode('utf-8'))
            if InputLetter == 'exit':
                print("EXITING")
                ClientSocket.send(str.encode(InputLetter))
                ClientSocket.close()
                sys.exit()
            print('astept1')
            ClientSocket.send(str.encode(InputLetter))
            print('trimis1')
            while True:
                print(ClientSocket.recv(2048).decode('utf-8'))
                msg = ClientSocket.recv(5000).decode('utf-8')
                if 'Cuvantul era: ' in msg:
                    print(msg)
                    break
                InputLetter = input(msg)
                if InputLetter == 'exit':
                    print("EXITING")
                    ClientSocket.send(str.encode(InputLetter))
                    ClientSocket.close()
                    sys.exit()
                print('astept')
                time.sleep(1)
                ClientSocket.send(str.encode(InputLetter))
                print('trimis')
