import socket
import errno, time

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
            ClientSocket.send(str.encode(Input))
            Input = input('Descriere: ')
            ClientSocket.send(str.encode(Input))
            # Play again
            msg = ClientSocket.recv(2048).decode('utf-8')

    if clientType == '2':

        print('2')
        while True:
            msg = ClientSocket.recv(2048).decode('utf-8')
            if msg == '\nWaiting for a word and description . . . ':
                time.sleep(1)
                print(msg)
                print(ClientSocket.recv(2048).decode('utf-8'))
            else:
                print(ClientSocket.recv(2048).decode('utf-8'))

            InputLetter = input(ClientSocket.recv(2048).decode('utf-8'))
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


                print('astept')
                time.sleep(1)
                ClientSocket.send(str.encode(InputLetter))
                print('trimis')
