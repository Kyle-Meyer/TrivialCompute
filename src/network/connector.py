import socket
import pickle

class connector(object):
    def __init__(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server #"localhost"
        self.port = port #5555
        self.addr = (self.server, self.port)
        self.obj = self.connect()

    def getObj(self):
        return self.obj
    
    #this only happens once at initial handshake
    def connect(self):
        try:
            print("CALLED CONNECT")
            self.client.connect(self.addr)
            print("RETURNING?")
            inObj = pickle.loads(self.client.recv(2048))
            if not inObj:
                print("BAD OBJECT RECEIVED!!!")
            else:
                print("typer: ", type(inObj))
            return inObj
        except Exception as error:
            print("ERROR: ", error)
            pass
    
    #the return of the function is the reply from the server
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print("balls", e)
        return -1
