import socket
import os
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
confirmCuvant = 0
cuvant = ''
descriere = ''
word_completion = ''
tries = 0
guessed = False
guessedLetters = []
guessedWords = []

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    global cuvant, descriere, confirmCuvant, word_completion, tries, guessed
    response = '1'
    connection.sendall(str.encode(response))
    cuvant = connection.recv(2048).decode('utf-8').upper()
    descriere = connection.recv(2048).decode('utf-8')
    confirmCuvant = 1
    word_completion = "_" * len(cuvant)


def multi_threaded_client2(connection):
    global guessedLetters, tries, word_completion, guessedWords,guessed
    response = '2'
    connection.sendall(str.encode(response))
    if confirmCuvant == 0:
        connection.sendall(str.encode('Waiting for a word and description . . . '))
    while True:
        if confirmCuvant > 0:
            connection.sendall(str.encode('Cuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere))
            break


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    if ThreadCount == 1:
        start_new_thread(multi_threaded_client, (Client,))
    if ThreadCount == 2:
        start_new_thread(multi_threaded_client2, (Client,))
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()
