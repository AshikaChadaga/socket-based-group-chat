import argparse
# from multiprocessing import Process
# from server import check_start_server
from client import Client

HOST = '127.0.0.1'
PORT = 8080

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("user")
    args = parser.parse_args()

    client = Client(HOST,PORT,args.user)
    client.start_client()


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("user")
#     args = parser.parse_args()
#
#     p = Process(target=check_start_server, args=(HOST,PORT))
#     p.start()
#
#     client = Client(HOST,PORT,args.user)
#     client.start_client()
#     p.join()
