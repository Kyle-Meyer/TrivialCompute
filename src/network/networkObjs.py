import socket
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
from colors import *

#the object the in control player sends
class startGame(object):
    def __init__(self, didstart):
        self.didStart = didstart

class initObject(object):
    def __init__(self, totalPlayers):
        self.totalPlayers = totalPlayers

class playerObj(object):
    def __init__(self, currState, playerNum, playerPos, dice, question, answer, base64_string, myVote, passTurn):
        self.state = currState
        self.id = playerNum
        self.position = playerPos
        self.dice = dice
        self.question = question
        self.answer = answer
        self.base64_string = base64_string
        self.passTurn = passTurn
        self.myVote = myVote
class observeObject:
    def __init__(self, id, vote):
        self.id = id
        self.vote = vote
class rollObj(object):
    def __init__(self, diceRoll):
        self.diceRoll = diceRoll

class serverObj(object):
    def __init__(self, controller, state, player1Pos, player2Pos, player3Pos, player4Pos, currentDice, question, answer, base64_string, player1Vote, player2Vote, player3Vote, player4Vote):
        self.state = state
        self.controller = controller
        self.player1Pos = player1Pos
        self.player2Pos = player2Pos
        self.player3Pos = player3Pos
        self.player4Pos = player4Pos
        self.dice = currentDice
        self.question = question
        self.answer = answer
        self.base64_string = base64_string
        self.player1Vote = player1Vote
        self.player2Vote = player2Vote
        self.player3Vote = player3Vote
        self.player4Vote = player4Vote
