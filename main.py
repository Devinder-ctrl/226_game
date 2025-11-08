#!/usr/bin/python3.11
from asyncio import run, start_server, StreamReader, StreamWriter
import asyncio
from random import randint
from Board import board
from Player import Player
from threading import Thread
from queue import Queue
import struct
import zlib
import re

HOST = ''
PORT = 12345

input_queue = asyncio.Queue()
output_queue = asyncio.Queue()

board_size = 10
treasures = 4
b = board(board_size, treasures) #creates a board
b.treasures()                    #place treasures on board
b.print_board() 


client = 0
    
async def inputs() -> None:
            #Two player objects
        player_one = Player('One')
        player_two = Player('Two')

        while True:
            new_client,row,column = await input_queue.get()#get user
            if row < 0 or row >= board_size or column < 0 or column >= board_size:
                #send binary number to player thread for invalid input
                t = 0b1100000000000000
                #put binary number in output queue to send it to player thread
                await output_queue.put(t)
                
                
            else:
                if new_client == 0:
                    score_one = b.pick(row, column)                        #get first players score using pick function from board
                    player_one.add_score(score_one)                        #add scores for player one
                   
                    t1 = player_one.get_score() << 7
                    t2 = player_two.get_score()
                    await output_queue.put(t1+t2)
                    b.print_board()
                    #bit shift by 7 to get 9 bits for player one score

                #similar to client 0 , player pick score which gets stored in add_score function
                #the getting its total
                elif new_client == 1:
                    score_two = b.pick(row, column)                          #get second players score using pick function from board
                    player_two.add_score(score_two)                          #add scores for player two
                    
                    t1 = player_one.get_score() << 7
                    t2 = player_two.get_score()
                    await output_queue.put(t1+t2)
                    b.print_board()
            print("First Players Score :", player_one.get_score())
            print("Second Players Score :", player_two.get_score())

async def board(board_str:str, writer) -> None:

        plain_board = re.sub(r'[\d]', '_', board_str)
        
        board_byte = plain_board.encode('utf-8')
        compressed_board = zlib.compress(board_byte, level=9)
        board_len = struct.pack("!H", len(compressed_board))
        writer.write(board_len)
        writer.write(compressed_board)
        await writer.drain()
        
async def handle_cnx(reader: StreamReader, writer: StreamWriter) -> None:
    global client
    
    curr_client = 0
    client += 1
    if client == 1:
        player_name = 'One'
        curr_client = 0
    elif client == 2:
        player_name = 'Two'
        curr_client = 1
    else:
        writer.close()
        await writer.wait_closed()
        return
    player = player_name.encode('utf-8')
    name_length = struct.pack('!H', len(player))  # unpack data
    writer.write(name_length)
    writer.write(player)
    await writer.drain()
    while True:
        data = await reader.readexactly(1)
                        # receive Data from the socket
        try:                                      #try-except to end game if no more treasure on board
            value = struct.unpack('!B', data)[0]  # unpack client input as unsigned char data (need 1 byte)
        except:
            print("Game End")
            exit()
            
        row = (value >> 4) & 0b1111           #shift the input by 4 and bitmask it to get row
        column = value & 0b1111               #bitmask remaining number to get column
        # if row < 0 or row >= board_size or column < 0 or column >= board_size:
        #     t = output_queue.get().decode()
        #     print(t)
        #     continue
        print("Clients IP:",  data.hex(), row, column)  # get clients ip,data hex,row and column
        await input_queue.put((curr_client, row, column))       #put the client,row and column in input_queue to send it to board thread
        t1 = await output_queue.get()        #get player's score from board thread using output_queue
        result_one = struct.pack('!H', t1)#then pack the result as unsigned short and send it to sock
        writer.write(result_one)
        await writer.drain()
        
        string_board = b.__str__()
        await board(string_board, writer)
                 
    writer.close()
    await writer.wait_closed() 


async def main() -> None:
    """
    Main function which is called on start
    starts server and creates the main task
    """

    server = await asyncio.start_server(handle_cnx, HOST, PORT)
    asyncio.create_task(inputs())

    await server.serve_forever()


run(main())