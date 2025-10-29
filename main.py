import struct
from socket import socket, AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
from Board import board
from Player import Player
from sys import argv
from threading import Thread
from queue import Queue

BUF_SIZE = 1024
HOST = ''
PORT = 12345

#Default board size and treasure
board_size = 10
treasures = 4


input_queue = Queue()
output_queue = Queue()
#server socket
def board_thread():
    b = board(board_size, treasures)
    b.treasures()

    b.printboard()

    player1 = Player('One')
    player2 = Player('Two')
    while True:

        (client, row,column) = input_queue.get()#get user


        if row < 0 or row >= board_size or column < 0 or column >= board_size:
                #Bits: 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
                # 1  1  0  0  0  0 0 0 0 0 0 0 0 0 0 0
                #2 front bits are 1 and remaining 0
                t = 0b1100000000000000
                #pack result
                #send result
                b.printboard()
                output_queue.put(t)

        else:
            #get score and add score


                if client == 0:
                    score1 = b.pick(row, column)
                    player1.add_score(score1)
                    print("Treasure Found for Player 1 :", score1)
                    print("First Players Score :", player1.get_score())

                    t1 = player1.get_score() << 7
                    t2 = player2.get_score()


                    output_queue.put(t1+t2)
                    b.printboard()


                elif client == 1:
                    score2 = b.pick(row, column)
                    player2.add_score(score2)

                    print("Treasure Found for Player 2 :", score2)
                    print("Second Players Score :", player2.get_score())
                    t1 = player1.get_score() << 7
                    t2 = player2.get_score()
                    output_queue.put(t1+t2)

                    b.printboard()







                #send score to client
                # playersScore = One.getScore()
                # S = playersScore.to_bytes(2,byteorder='big')
                # ScoreByte = struct.pack('!H', S)
                # sc.send(ScoreByte)





def player_thread1(sc, client):

    # handle connection
        #send name length to client

        if client == 0:

            player_name = 'One'
            player_one = player_name.encode('utf-8')
            length = struct.pack('!H', len(player_one))  # unpack data
            sc.sendall(length)
            sc.sendall(player_one)
            while True:
                data = sc.recv(BUF_SIZE)  # receive message with 1 byte of size
                value = struct.unpack('!B', data)[0]  # unpack struct, get data as an unsigned char as we need only 1 byte
                row = (value >> 4) & 0b1111  # shift to 4 bits
                column = value & 0b1111  # remaining binary numbers goes to columns

                print("Clients IP:", sc.getsockname(), data.hex(), row, column)  # get clients ip, hex,row and columns

                input_queue.put((client, row, column))

                t1 = output_queue.get()

                result1 = struct.pack('!H', t1)
                sc.send(result1)

        else:
            player_name = 'Two'
            player_one = player_name.encode('utf-8')
            length = struct.pack('!H',len(player_one)) #unpack data
            sc.send(length)
            sc.send(player_one)
            while True:
                data = sc.recv(BUF_SIZE)  # receive message with 1 byte of size
                value = struct.unpack('!B', data)[0]  # unpack struct, get data as an unsigned char as we need only 1 byte
                row = (value >> 4) & 0b1111  # shift to 4 bits
                column = value & 0b1111  # remaining binary numbers goes to columns

                print("Clients IP:", sc.getsockname(), data.hex(), row, column)  # get clients ip, hex,row and columns

                #row s and columns
                input_queue.put((client,row, column))

                #get score
                t2 = output_queue.get()
                #send it to client
                result2 = struct.pack('!H', t2)
                sc.send(result2)






with socket(AF_INET, SOCK_STREAM) as sock:  # AF_INET = IPv4, SOCK_STREAM = TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # ALLOW REUSE OF ADDRESS
    sock.bind((HOST, PORT))  # bind socket to port
    sock.listen(2)  # listen for connection at port one

    client = 0
    Thread(target=board_thread).start()
    while True:
        if client < 2:

            sc, _ = sock.accept()  # wait for client to connect
            # sendClient = struct.pack('!H', client)
            # sc.send(sendClient)
            Thread(target=player_thread1, args=(sc,client)).start()
            client += 1


