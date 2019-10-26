This is a group chat application implemented using Sockets (TCP) and threads. 

server.py:
	Implements a multi threaded broadcast server that can handle multiple client connections. 

client.py:
	Receives messages from server and contains a blocking thread which takes user input and sends to server.

chat.py:
	starts the client
