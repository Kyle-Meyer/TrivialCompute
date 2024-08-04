import socket
import pickle

class connector(object):
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.obj = self.connect()

    def getObj(self):
        return self.obj
    
    #this only happens once at initial handshake
    def connect(self):
        try:
            print("CALLED")
            self.client.connect(self.addr)
            inObj = pickle.loads(self.client.recv(2048))
            return inObj
        except:
            pass
    
    #the return of the function is the reply from the server
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
