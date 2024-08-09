import socket
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from _thread import *
from network.networkObjs import *
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

soc.listen(4) #number of connections to listen 
print("waiting for connection, server, started")

def dumpData(inData):
    print("current state: ", inData.state)
    print("current player: ", inData.id)
    print("current coords of said player: ", inData.position)

#this is bad
players = [(757,328), (774,311), (791,328), (774,345)]
votes = [-1,-1,-1,-1]
states = [0,0,0,0]
controllingPlayer = 0
currState = 0
currRoll = 0
currQuestion = ''
currAnswer = ''
currBase64String = None
totalPlayers = 0
#now to make a threaded function
def threaded_client(conn, player):
    global currentPlayer
    global hasStarted
    global controllingPlayer
    global currState
    global currRoll
    global currQuestion
    global currAnswer
    global currBase64String
    global votes
    global totalPlayers
    #load the player object as a pickle object
    print("==============================")
    print("sending...", players[player])
    print(type(players[0]))
    handShakeObj = playerObj(0, player, (0,0), 0, '', '', None, -1, False)
    conn.sendall(pickle.dumps(handShakeObj))
    print("threaded client started")
    if player == 0: #if the controller reconnects to the server
        currState = 0
        controllingPlayer = 0
    reply = ""
    n = 0
    while True:
        try:
            #print("trying")
            #receive data as an object
            data = pickle.loads(conn.recv(2048))
            if not data:
                print("bad data, breaking")
                break
            #TODO change this to send more than one players data
            if isinstance(data, initObject):
                totalPlayers = data.totalPlayers

            if isinstance(data, rollObj):
                if data.id == controllingPlayer:
                    currRoll = data.diceRoll
            elif isinstance(data, playerObj):
                players[data.id] = data.position
                currState = data.state
                if data.passTurn:
                    print("PASSING TURN")
                    controllingPlayer += 1
                    if controllingPlayer >= totalPlayers: #change this later, server needs to be aware of how many people there are
                        controllingPlayer = 0
                if data.state == 0:
                    votes = [-1, -1, -1, -1]
                currRoll = data.dice
                currQuestion = data.question
                currAnswer = data.answer
                currBase64String = data.base64_string
                #print("received: ", data)
                #dumpData(data)
                #print("sending: ", reply)
                #print("type: ", type(reply.player1Pos))
            elif isinstance(data, observeObject):
                '''print("PLAYERS: ", players, 
                      "STATE: ", currState, 
                      " CONTROLLER = ", controllingPlayer, 
                      "DICE: ", currRoll,
                      "Question: ", currQuestion, 
                      "Answer: ", currAnswer,
                      "Votes: ", votes,
                      "BEING SENT TO: ", data.id)'''
                votes[data.id] = data.vote
            reply = serverObj(controllingPlayer,
                                currState, 
                                players[0], 
                                players[1], 
                                players[2], 
                                players[3], 
                                currRoll, 
                                currQuestion, 
                                currAnswer,
                                currBase64String,
                                votes[0],
                                votes[1],
                                votes[2],
                                votes[3])
            conn.sendall(pickle.dumps(reply))
        except Exception as error:
            print("exception call: ", error)
            break
    print("closing connection")
    currentPlayer -= 1
    conn.close()

currentPlayer = 0

hasStarted = False
while True:
    conn, addr = soc.accept() #blindly accept any connection
    print("connected to: ", addr)
    print("connection: ", conn)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    if hasStarted:
        soc.close()
        print("no more connections")
        sys.exit()
    

