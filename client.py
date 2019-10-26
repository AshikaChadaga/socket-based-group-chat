import socket
import logging
import threading

MSG = ""
KILL = False

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
_logger.setLevel(logging.DEBUG)

class Client:
    def __init__(self,host,port,user):
        self.host=host
        self.port=port
        self.user=user
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def start_client(self):

        retry = 0
        while True:
            try:
                self.client.connect((self.host, self.port))
                break
            except Exception:
                retry += 1
                if retry >= 100:
                    self.client.close()
                    return "failed"

        self.client.sendall(bytes(self.user +" logging in" , 'UTF-8'))
        t=threading.Thread(target=self.send_thread)
        t.start()

        while True:
            in_data = self.client.recv(1024)
            if in_data.decode() != MSG:
                print(in_data.decode())
            if KILL:
                break

        self.client.close()

    def send_thread(self):
        global MSG, KILL
        while True:
            out_data = input()
            MSG = self.user + ": " + out_data
            self.client.sendall(bytes(MSG, 'UTF-8'))
            if out_data == 'bye':
                KILL = True
                break



