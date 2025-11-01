#---------Game Server-----------#
from socket import socket, AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
from Board import board
from Player import Player
from threading import Thread
from queue import Queue
import struct

BUF_SIZE = 1024  #size of data buffer
HOST = ''        #listen on all networks
PORT = 12345     #accept connections on this port


#Queues for communication between threads
input_queue = Queue() #store input data
output_queue = Queue()#store output data


#------Board Thread --------#
def board_thread():

    """
    Board thread for managing board
    Get inputs from players , updates the board,
    return scores and sends result back to players
    :return: None
    """

    #Default board size and Number of treasures
    board_size = 10
    treasures = 4
    b = board(board_size, treasures) #creates a board
    b.treasures()                    #place treasures on board
    b.print_board()                   #prints the board

    #Two player objects
    player_one = Player('One')
    player_two = Player('Two')

    #----------main loop------------#
    while True:
        #get row,column and client tuple from player thread
        (client,row,column) = input_queue.get()#get user

        #----validate coordinates----#
        if row < 0 or row >= board_size or column < 0 or column >= board_size:
                #send binary number to player thread for invalid input
                t = 0b1100000000000000
                #put binary number in output queue to send it to player thread
                output_queue.put(t)

        else:
                #validate client number if its 0 or 1
                if client == 0:
                    score_one = b.pick(row, column)                        #get first players score using pick function from board
                    player_one.add_score(score_one)                        #add scores for player one
                    print("Treasure Found for Player 1 :", score_one)      #print its treasure and players total score
                    print("First Players Score :", player_one.get_score())

                    #bit shift by 7 to get 9 bits for player one score
                    t1 = player_one.get_score() << 7
                    #left 7 bits for player 2 score
                    t2 = player_two.get_score()

                    #combine both player's score and put it in output_queue for board thread
                    output_queue.put(t1 + t2)
                    #print updated board
                    b.print_board()

                #similar to client 0 , player pick score which gets stored in add_score function
                #the getting its total
                elif client == 1:
                    score_two = b.pick(row, column)                          #get second players score using pick function from board
                    player_two.add_score(score_two)                          #add scores for player two
                    print("Treasure Found for Player 2 :", score_two)        #print its treasure and players total score
                    print("Second Players Score :", player_two.get_score())

                    t1 = player_one.get_score() << 7
                    t2 = player_two.get_score()
                    output_queue.put(t1+t2)
                    b.print_board()

#----------Player Thread-----------#
def player_thread(sc, client):

        """
        Player thread send and receive data from board using queues,
        it communicates with client to receive data and inputs,
        It has two players run back and forth depending on the client's number

        :param sc: Socket object connected to client
        :param client: Player's Client number (0 or 1)
        :return:None
        """

        if client == 0:
            player_name = 'One'
            player = player_name.encode('utf-8')
            name_length = struct.pack('!H', len(player))  # unpack data
            sc.send(name_length)
            sc.send(player)
            while True:
                data = sc.recv(BUF_SIZE)                  # receive Data from the socket
                try:                                      #try-except to end game if no more treasure on board
                    value = struct.unpack('!B', data)[0]  # unpack client input as unsigned char data (need 1 byte)
                except:
                    print("Game End")
                    exit()
                row = (value >> 4) & 0b1111           #shift the input by 4 and bitmask it to get row
                column = value & 0b1111               #bitmask remaining number to get column
                print("Clients IP:", sc.getsockname(), data.hex(), row, column)  # get clients ip,data hex,row and column
                input_queue.put((client, row, column))       #put the client,row and column in input_queue to send it to board thread
                t1 = output_queue.get()        #get player's score from board thread using output_queue
                result_one = struct.pack('!H', t1)#then pack the result as unsigned short and send it to sock
                sc.send(result_one)

        else:
            player_name = 'Two'
            player = player_name.encode('utf-8')
            name_length = struct.pack('!H', len(player))  
            sc.send(name_length)
            sc.send(player)
            while True:
                data = sc.recv(BUF_SIZE)
                try:
                     value = struct.unpack('!B', data)[0]
                except:
                    print("Game End")
                    exit()
                row = (value >> 4) & 0b1111
                column = value & 0b1111
                print("Clients IP:", sc.getpeername(), data.hex(), row, column)
                input_queue.put((client,row, column))
                t2 = output_queue.get()
                result_two = struct.pack('!H', t2)
                sc.send(result_two)



#------------server---------------#
with socket(AF_INET, SOCK_STREAM) as sock:  # AF_INET = IPv4, SOCK_STREAM = TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # ALLOW REUSE OF ADDRESS
    sock.bind((HOST, PORT))  # bind socket to port
    sock.listen(2)  # listen for connection on 2 ports only
    client = 0
    Thread(target=board_thread).start() #start board thread
    while True:
            sc, _ = sock.accept() #accept connection
            #number of clients shoulb be less that 2 else close the socket connection to that client
            if client < 2:
                #start player thread by passing parameters sock and client
                Thread(target=player_thread, args=(sc,client)).start()
                client += 1
            else:
                sc.close()

