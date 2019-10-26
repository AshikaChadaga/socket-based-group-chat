import socket
import threading
import logging
import redis

HOST = '127.0.0.1'
PORT = 8080
r = redis.Redis(host='localhost', port=6379, db=0)
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
_logger.setLevel(logging.DEBUG)

CLIENT_SOCKETS = {}
USER_DICT = {}


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def leader_check(self):
        try:
            lc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lc.connect((self.host, self.port))
            lc.close()
            return False
        except Exception:
            return True

    def server_start(self):
        global CLIENT_SOCKETS
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        _logger.info("Server started. Waiting for client request..")

        while True:
            server.listen(1)
            sock, Address = server.accept()
            socket_key = Address[0] + ":" + str(Address[1])
            CLIENT_SOCKETS[socket_key] = {"sock": sock, "addr": Address}
            r.set(socket_key, 1)
            newthread = ClientThread(Address, sock)
            newthread.start()


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        self.key = clientAddress[0] + ":" + str(clientAddress[1])
        _logger.info("New connection added: %s", clientAddress)

    def run(self):
        global USER_DICT
        _logger.info("Connection from : %s", self.clientAddress)
        user = ""
        while True:
            data = self.csocket.recv(2048)
            if data == b"" or data.decode() == "bye":
                r.delete(self.key)
                del USER_DICT[user]
                break
            if user == "":
                if len(USER_DICT) == 0:
                    self.csocket.send(bytes("you are the first one here", "UTF-8"))
                else:
                    self.csocket.send(
                        bytes("follwing users are already in the group - {}".format(list(USER_DICT.keys())), "UTF-8"))
                info = data.decode()
                user = info.split(" ")[0]
                USER_DICT[user] = 1

            msg = data.decode()
            if msg == 'bye':
                break

            _logger.info("Server got - %s", msg)
            for key in r.scan_iter("*"):
                value = CLIENT_SOCKETS[key.decode()]
                _logger.warning("sending back to client - %s", value["addr"])
                value["sock"].send(bytes(msg, 'UTF-8'))
        _logger.info("Client at %s is disconnected...", self.clientAddress)


def check_start_server(host, port):
    server = Server(host, port)
    check = server.leader_check()
    if check:
        r.flushall()
        server.server_start()
    else:
        _logger.error("server already exists")


if __name__ == "__main__":
    check_start_server(HOST, PORT)
