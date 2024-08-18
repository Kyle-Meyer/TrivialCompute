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


server  = configModule.serverName
port = configModule.serverPort

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#this runs a basic server
try:
    soc.bind((server, port))
except socket.error as e:
    str(e)
    print(e)

soc.listen(4) #number of connections to listen 
print("waiting for connection, server, started")

def setServer(inServer):
    server = inServer
def setPort(inPort):
    port = inPort

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
currQuestionId = None
totalPlayers = 0
gameData = {}
trivMenuStatus = False
#now to make a threaded function
def threaded_client(conn, player):
    global currentPlayer
    global hasStarted
    global controllingPlayer
    global currState
    global currRoll
    global currQuestionId
    global votes
    global totalPlayers
    global gameData
    global trivMenuStatus
    #load the player object as a pickle object
    print("==============================")
    print("sending...", players[player])
    print(type(players[0]))
    handShakeObj = playerObj(0, player, (0,0), 0, None, -1, False, False)
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
                print(data.initDictionary)
                #totalPlayers = data.totalPlayers
                gameData = data.initDictionary
                totalPlayers = data.initDictionary["number_of_players"]
                print("SETTING TOTAL PLAYERS TO: ", totalPlayers)
                
            if isinstance(data, rollObj):
                if data.id == controllingPlayer:
                    currRoll = data.diceRoll
            elif isinstance(data, playerObj):
                players[data.id] = data.position
                currState = data.state
                trivMenuStatus = data.trivMenuOut
                if data.passTurn:
                    #print("PASSING TURN")
                    controllingPlayer += 1
                    data.state = 0
                    if controllingPlayer >= totalPlayers: #change this later, server needs to be aware of how many people there are
                        controllingPlayer = 0
                if data.state == 0:
                    votes = [-1, -1, -1, -1]
                currRoll = data.dice
                currQuestionId = data.questionId
                #print("received: ", data)
                #dumpData(data)
                #print("sending: ", reply)
                #print("type: ", type(reply.player1Pos))
            elif isinstance(data, observeObject):
                '''print("PLAYERS: ", players, 
                      "STATE: ", currState, 
                      " CONTROLLER = ", controllingPlayer, 
                      "DICE: ", currRoll,
                      "Question Id: ", currQuestionId, 
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
                                currQuestionId,
                                votes[0],
                                votes[1],
                                votes[2],
                                votes[3],
                                trivMenuStatus)
            
            if isinstance(data, joinObject):
                print("SENDING ", gameData)
                reply = initObject(gameData)
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
    

