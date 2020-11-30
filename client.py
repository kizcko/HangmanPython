import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233
gameover = 0
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))





while True:
    Response = ClientSocket.recv(1024)
    clientType = Response.decode('utf-8')
    if clientType == '1':
        Input = input('Cuvantul pentru Spanzuratoare: ')
        ClientSocket.send(str.encode(Input))
        Input = input('Descriere: ')
        ClientSocket.send(str.encode(Input))
        print(ClientSocket.recv(1024).decode('utf-8'))
    if clientType == '2':
        msg = ClientSocket.recv(1024).decode('utf-8')
        if msg == 'Waiting for a word and description . . . ':
            print(msg)
            print(ClientSocket.recv(1024).decode('utf-8'))
        else:
            print(ClientSocket.recv(1024).decode('utf-8'))

        InputLetter = input(ClientSocket.recv(1024).decode('utf-8'))
        ClientSocket.send(str.encode(InputLetter))
        while True:
            msg = ClientSocket.recv(1024).decode('utf-8')
            if msg == 'Ai ghicit cuvantul' or msg == 'Ai pierdut':
                print(msg)
                break
            print(msg)
            InputLetter = input(ClientSocket.recv(1024).decode('utf-8'))
            ClientSocket.send(str.encode(InputLetter))



ClientSocket.close()