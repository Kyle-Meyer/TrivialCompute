import socket
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from _thread import *
from networkObjs import *
import pickle
from colors import *


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


players = [netWorkObj(), netWorkObj(), netWorkObj(), netWorkObj()]
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
            players[data.id] = data
            if not data:
                #print("bad connection from: ", conn)
                break
            #TODO change this to send more than one players data
            else:
                reply = players
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