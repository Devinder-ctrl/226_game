#The client must:



# convey that information to the server
# show the latest scores provided by the server


from socket import socket,AF_INET, SOCK_STREAM
from sys import argv
import struct

HOST ='10.21.75.55'
BUF_SIZE = 1024
PORT = 12345

#initially contact the server to get a player name. To allow for efficient transmission, the length of the player name must be
# sent as a packed unsigned short before sending the player name. This also requires an update to the server code

def receive(sc, size):
    data = b''
    while len(data) < size:
        curr_data = sc.recv(size - len(data))
        if curr_data == b'':
            return data
        data += curr_data
    return data


with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))# CONNECTION


    nameLength = receive(sock,2)
    Length = struct.unpack('!H',nameLength )[0]
    name = receive(sock,Length).decode('utf-8')

    print(name)
    total = 0
    while True:

        row = int(input('Enter a row: \n'))
        col = int(input("Enter a column: \n"))
        number = (row << 4) | col
        rowColumnBit = struct.pack('!B',number)
        sock.sendall(rowColumnBit)

        if  name == "One":
            T1 = receive(sock,2)
            Score1 = struct.unpack('!H',T1)[0]
            score = (Score1 & 0b11111110000000) >> 7
            final_score = int(score)
            print("Score for player 1: " ,score)

        elif name == "Two":
            T2 = receive(sock, 2)
            Score2 = struct.unpack('!H', T2)[0]
            score = (Score2 & 0b1111111)
            print("Score for player 2: ", int(score))



# keep the connection to the server open unless an error occurs




# repeatedly prompt the user for a row and a column

    # T = sock.recv(BUF_SIZE)
    #
    # ScoreFromServer = struct.unpack('!H',T)
    # ScoreFinal = ScoreFromServer


    # s = sock.recv(BUF_SIZE)
    # score = struct.unpack('!H', s)





