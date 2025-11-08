#------------Game Client--------------#
from socket import socket,AF_INET, SOCK_STREAM
import struct
import zlib
from queue import Queue
HOST =''
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
    total_score = 30
    print(player_name)
    while True:
        # get client's input for row and column
            row = int(input('Enter a row: \n'))
            #validate row range
            if row < 0 or row >= board_size :
                print("Row not in range")
                continue
            
                #validate column range
            while True:
                col = int(input("Enter a column: \n"))

                if  col < 0 or col >= board_size:
                    print("Column not in range")
                    continue
                    #bit shift row by 4 and add it to column
                
                else:
                    row_col = (row << 4) | col 
                    row_column_bit = struct.pack('!B', row_col)  # pack the row and column as an unsigned char
                    sock.sendall(row_column_bit)                 # send it to socket
                    binary_score = receive(sock, 2)
                    score = struct.unpack('!H', binary_score)[0]
                    score_one = (score & 0b11111110000000) >> 7
                    score_two = (score & 0b1111111)

                    board_bytes = receive(sock,2)   #recive binary
                    board_length = struct.unpack('!H', board_bytes)[0]
                    compressed_board = receive(sock,board_length) #recive binary length\
                    
                    #unpack board length to receive

                    board_data = zlib.decompress(compressed_board).decode('utf-8')
                    print("Score for player 1:", int(score_one))
                    print("Score for player 2:", int(score_two))
                    print(board_data)
                    
                break
                # validate player's name
                # receive score from socket and unpack it as unsigned short
                # then bitmask the score and bit shift the extracted score by 7 to get first player score
                # then bitmask the remaing digits to get second player's score

               
                    

                #loop till total score is 30 and print both players score
                
          







