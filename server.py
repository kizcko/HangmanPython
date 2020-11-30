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
    tries = 6
    guessed = False
    while True:
        if guessed == True:
            connection.sendall(str.encode('A ghiciti cuvantul'))
            break
        if tries == 0 and guessed == False:
            connection.sendall(str.encode('Nu a ghicit cuvantul'))
            break


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

    while tries > 0 and not guessed:
        connection.sendall(str.encode('Litera: '))
        guess = connection.recv(2048).decode('utf-8').upper()
        if len(guess) == 1:
            if guess in guessedLetters:
                connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere + '\nDeja incercat'))
            elif guess not in cuvant :
                tries -= 1
                guessedLetters.append(guess)
                connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere + '\nLitera gresita'))
            else:
                guessedLetters.append(guess)
                wordToList = list(word_completion)
                for i in range(len(cuvant)):
                    if cuvant[i] == guess:
                        wordToList[i] = guess.upper()
                word_completion = "".join(wordToList)
                connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere))
        if len(guess) == len(cuvant):
            if guess in guessedWords:
                connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere + '\nDeja incercat'))
            elif guess != cuvant :
                tries -= 1
                guessedWords.append(guess)
                connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere + '\nCuvant gresit'))
            else:
                word_completion = cuvant
                connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere))

        if len(guess) > 1:
            connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere + '\nPoti pune o litera sau tot cuvantul doar'))
        if word_completion == cuvant:
            guessed = True


    if guessed == True:
        connection.sendall(str.encode('Ai ghicit cuvantul'))
    else:
        connection.sendall(str.encode('Ai pierdut'))




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
