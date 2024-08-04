import socket
from _thread import *
import sys
from player import player
import pickle

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

server  = "localhost"
port = 5555

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#this runs a basic server
try:
    soc.bind((server, port))
except socket.error as e:
    str(e)
    print(e)

soc.listen(2) #number of connections to listen 

print("waiting for connection, server, started")


players = [player((50,50), 10, 10, RED), player((90,90), 10, 10, GREEN)]
#now to make a threaded function
def threaded_client(conn, player):
    global currentPlayer
    #load the player object as a pickle object
    conn.send(pickle.dumps(players[player]))
    print("threaded client started")
    reply = ""
    n = 0
    while True:
        try:
            #receive data as an object
            data = pickle.loads(conn.recv(2048))
            players[player] = data
            if not data:
                #print("bad connection from: ", conn)
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("received: ", data)
                print("sending: ", reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("closing connection")
    currentPlayer -= 1
    conn.close()

currentPlayer = 0
while True:
    conn, addr = soc.accept() #blindly accept any connection
    print("connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1