#------------Game Client--------------#
from socket import socket,AF_INET, SOCK_STREAM
import struct
from queue import Queue
HOST ='10.21.75.55'
BUF_SIZE = 1024
PORT = 12345


def receive(sc, size):
    """
    checks if data length is smaller than the size ,
    get current data by subtracting received data size and length the of data,
    returns whole data
    :param sc: socket to get size
    :param size: size
    :return: data
    """
    data = b''
    while len(data) < size:
        curr_data = sc.recv(size - len(data))
        if curr_data == b'':
            return data
        data += curr_data
    return data

#------------Client-------------#
with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))                        #create connection
    name_length = receive(sock,2)                    #get name length from socket using receive function
    try:                                             #try-except to print error if number of client if more than 2
        Length = struct.unpack('!H',name_length )[0] #unpack length as an unsigned char
    except:
        print("Connection refused")
        exit()
    player_name = receive(sock,Length).decode('utf-8')#receive name and decode it
    board_size = 10
    print(player_name)
    while True:
        # get client's input for row and column
            row = int(input('Enter a row: \n'))
            #validate row range
            if row < 0 or row >= board_size :
                raise Exception("Row and Column are not in range")
            else:
                col = int(input("Enter a column: \n"))
                #validate column range
                if 0 <= col < board_size: 
                    #bit shift row by 4 and add it to column
                    row_col = (row << 4) | col 
                    row_column_bit = struct.pack('!B', row_col)  # pack the row and column as an unsigned char
                    sock.sendall(row_column_bit)                 # send it to socket

                    # validate player's name
                    # receive score from socket and unpack it as unsigned short
                    # then bitmask the score and bit shift the extracted score by 7 to get first player score
                    # then bitmask the remaing digits to get second player's score
                    binary_score = receive(sock, 2)
                    score = struct.unpack('!H', binary_score)[0]
                    score_one = (score & 0b11111110000000) >> 7
                    score_two = (score & 0b1111111)
                    
                    #loop till total score is 30 and print both players score
                    if(score_one + score_two != 30):
                        if player_name == "One":
                            print("Score for player 1:", int(score_one))
                            print("Score for player 2:", int(score_two))
                        elif player_name == "Two":
                            print("Score for player 1:", int(score_one))
                            print("Score for player 2:", int(score_two))
                    else:
                        #if one of the score is greater than the other player's score
                        #then that player becomes winner and close the connection
                        if(score_one > score_two):
                                print("Winner : One" )
                            
                        else:
                                print("Winner : Two")
                        exit()
                else:
                    # exception - if row and column are not in range
                    raise Exception("Row and Column are not in range")








