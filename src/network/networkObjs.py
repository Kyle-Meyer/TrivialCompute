import socket
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
from colors import *

class playerState(object):
    def __init__(self, inPos = (100, 100), inSize = (50,50)):
        self.position=inPos
        self.size = inSize

class netWorkObj(object):
    def __init__(self, currState, playerNum, playerPos):
        self.state = currState
        self.id = playerNum
        self.position = playerPos
