import socket
import os
from _thread import *
import errno, time
import sys
from subprocess import call

ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
play1 = 1
play2 = 1
score = 0
play2_exit = 0
play1_exit = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(2)


def reset():
    global confirmCuvant, cuvant, descriere, word_completion, tries, guessed, guessedLetters, guessedWords
    confirmCuvant = 0
    cuvant = ''
    descriere = ''
    word_completion = ''
    tries = 0
    guessed = False
    guessedLetters = []
    guessedWords = []


def init_send_cuvant(connection):
    global cuvant, descriere, confirmCuvant, word_completion, tries, guessed, play1

    cuvant = connection.recv(2048).decode('utf-8').upper()
    descriere = connection.recv(2048).decode('utf-8')
    confirmCuvant = 1
    word_completion = "_" * len(cuvant)
    tries = 6
    guessed = False


def game_client1(connection):
    global guessed, tries, play2_exit, play1_exit, ThreadCount
    while True:
        init_send_cuvant(connection)

        while True:
            if play2_exit == 1:
                connection.sendall(str.encode('\nS-a deconectat jucatorul'))
                play1_exit = 1
                ThreadCount -= 1
                print('Thread Number: ' + str(ThreadCount))
                reset()
                return
            if guessed:
                connection.sendall(str.encode('\nA ghiciti cuvantul'))
                break
            if tries == 0 and guessed == False:
                connection.sendall(str.encode('\nNu a ghicit cuvantul'))
                break


def multi_threaded_client(connection):
    global play1, score, confirmCuvant, play2
    response = '1'
    connection.sendall(str.encode(response))
    game_client1(connection)
    connection.close


def game_client2(connection):
    global word_completion, guessed, score, tries, play2, ThreadCount, play2_exit
    while True:
        if confirmCuvant == 0:
            time.sleep(1)
            connection.sendall(str.encode('\nWaiting for a word and description . . . '))
            time.sleep(1)

        while True:
            if confirmCuvant > 0:
                print('waiting')
                connection.sendall(
                    str.encode('Cuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere))
                time.sleep(1)
                print('trimis')
                break

        while tries > 0 and not guessed:
            connection.sendall(str.encode('\nLitera: '))
            time.sleep(1)
            guess = connection.recv(2048).decode('utf-8').upper()

            if guess.upper() == 'EXIT':
                play2_exit = 1
                print('Client exit')
                ThreadCount -= 1
                print('Thread Number: ' + str(ThreadCount))
                return

            print('primit')
            if len(guess) == 1:
                if guess in guessedLetters:
                    connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(
                        tries) + '\nDescriere: ' + descriere + '\nDeja incercat'))
                    time.sleep(1)
                    print('trimis')
                elif guess not in cuvant:
                    tries -= 1
                    guessedLetters.append(guess)
                    connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(
                        tries) + '\nDescriere: ' + descriere + '\nLitera gresita'))
                    time.sleep(1)
                    print('trimis')
                else:
                    guessedLetters.append(guess)
                    wordToList = list(word_completion)
                    for i in range(len(cuvant)):
                        if cuvant[i] == guess:
                            wordToList[i] = guess.upper()
                    word_completion = "".join(wordToList)
                    connection.sendall(
                        str.encode(
                            '\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere))
                    time.sleep(1)
                    print('trimis')
            if len(guess) == len(cuvant):
                if guess in guessedWords:
                    connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(
                        tries) + '\nDescriere: ' + descriere + '\nDeja incercat'))
                    time.sleep(1)
                    print('trimis')
                elif guess != cuvant:
                    tries -= 1
                    guessedWords.append(guess)
                    connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(
                        tries) + '\nDescriere: ' + descriere + '\nCuvant gresit'))
                    time.sleep(1)
                    print('trimis')
                else:
                    word_completion = cuvant
                    connection.sendall(
                        str.encode(
                            '\nCuvant: ' + word_completion + '\nTries: ' + str(tries) + '\nDescriere: ' + descriere))
                    time.sleep(1)
                    print('trimis')

            if 1 < len(guess) < len(cuvant) or 1 < len(guess) > len(cuvant):
                connection.sendall(str.encode('\nCuvant: ' + word_completion + '\nTries: ' + str(
                    tries) + '\nDescriere: ' + descriere + '\nPoti pune o litera sau tot cuvantul doar'))
                time.sleep(1)
                print('trimis')
            if word_completion == cuvant:
                guessed = True

        if guessed:
            score += 1
            connection.sendall(
                str.encode('\nScorul: ' + str(score) + '\nCuvantul era: ' + cuvant + '\nAi ghicit cuvantul'))
            reset()

        else:
            connection.sendall(str.encode('\nScorul: ' + str(score) + '\nCuvantul era: ' + cuvant + '\nAi pierdut'))
            reset()


def multi_threaded_client2(connection):
    global guessedLetters, tries, word_completion, guessedWords, guessed, play2, score, ThreadCount
    response = '2'
    connection.sendall(str.encode(response))
    score = 0
    game_client2(connection)
    connection.close


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    if ThreadCount == 10:
        break
    if ThreadCount == 1:
        start_new_thread(multi_threaded_client, (Client,))
    if ThreadCount == 2:
        start_new_thread(multi_threaded_client2, (Client,))

    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()
sys.exit()
