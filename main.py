import struct
from socket import socket, AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
from Board import board
from Player import Player
from sys import argv


BUF_SIZE = 1024
HOST = '10.21.75.55'  #listen on all network interfaces not just localhost
PORT = 12345

#get the board size and number of treasures
if (len(argv) >= 3):
    board_size = int(argv[1])
    treasures = int(argv[2])
else:
    board_size = 10
    treasures = 4


#server socket
with socket(AF_INET, SOCK_STREAM) as sock:# AF_INET = IPv4, SOCK_STREAM = TCP socket
    sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#ALLOW REUSE OF ADDRESS
    sock.bind((HOST, PORT)) #bind socket to port
    sock.listen(1)#listen for connection at port one

    #create board in socket
    b = board(board_size, treasures)
    b.treasures()
    b.printboard()

    # creating a player Object 'One' in socket
    One = Player('1')

    while True:
            sc,_ = sock.accept()  #wait for client to connect
            with sc:  # handle connection
                data = sc.recv(1)  # receive message with 1 byte of size
                value = struct.unpack('!B', data)[0]  # unpack struct, get data as an unsigned char as we need only 1 byte
                row = (value >> 4) & 0b1111  # shift to 4 bits
                column = value & 0b1111 # remaining binary numbers goes to columns
                print("Clients IP:", sc.getsockname(),data.hex() ,row,column)  # get clients ip, hex,row and columns



                # row = int(input('Enter a row \n'))
                # column = int(input('Enter a column \n'))

                # check if row and column is valid
                if row < 0 or row >= board_size or column < 0 or column >= board_size:
                      #Bits: 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
                            # 1  1  0  0  0  0 0 0 0 0 0 0 0 0 0 0
                    #2 front bits are 1 and remaining 0
                    t = 0b1100000000000000
                    #pack result
                    result = struct.pack('!H',t) #!H= unsigned short(16 bits)
                    #send result
                    sc.sendall(result)
                else:
                    #get score and add score
                    score = b.pick(row, column)
                    One.add_score(score)
                    print("Treasure Found :", score)
                    print("Players Score :", One.get_score())

                    b.printboard()
                    t = One.get_score() << 7

                    result = struct.pack('!H', t)
                    sc.sendall(result)








