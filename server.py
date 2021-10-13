"""
    !/bash/python3/

    A chat server

    SITES USED:
        https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
        https://docs.python.org/3/library/select.html
        https://docs.python.org/3/library/socket.html
        https://www.youtube.com/watch?v=Lbfe3-v7yE0
        https://www.youtube.com/watch?v=CV7_stUWvBQ
        https://stackoverflow.com/questions/25447803/python-socket-connection-exception

    Sean Ebenmelu (sce22)
    09/29/2021
"""

import socket, select, argparse, sys

# Read options from command line
parser = argparse.ArgumentParser(description="A prattle server")

parser.add_argument("-p", "--port", dest="port", type=int, default=12345,
                    help="TCP port the server is listening on (default 12345)")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                    help="turn verbose output on")
args = parser.parse_args()

BUFFERSIZE = 10

def makeSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    server = makeSocket()    # creates a socket

    port = args.port

    # if current port not in use the socket can be bound, else
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((socket.gethostname(), port)) # REM: hostname is the IP Address

        # listens on port, while at the same time has a backlog for max queue
        server.listen()

    # Code by Ifeanyichukwu (iko2) '''

    except socket.error:
        print("Couldn't Connect.")
    except OSError:
        print("Port in use.")
    except OverflowError:
        print("Exceeded Port Range")
    # '''

    socks = [server] # adds current socket to list of sockets

    while True:
        try:
            # Code by Ifeanyichukwu (iko2)
            readWhen, write, exception = select.select(socks, [], []) # holds a queue of an array of sockets, exceptions, and waiting messages

            for client in readWhen: # runs through list of sockets
                if client == server:
                    clientSocket, clientAddr = server.accept()  # accept incoming connection

                    socks.append(clientSocket)
                    clientSocket.send('Thank you for connecting'.encode('utf-8'))

                else:
                    # call recv(1024 on the socket)
                    try:
                        msg = server.recv(1024).decode("utf-8")
                        if len(msg) == 0:
                            raise RuntimeError  # checks if a user has disconnected
                    except RuntimeError:
                        print("A user has disconnected...")
                    # if result is bad, rem socket from socks
                    if not msg:
                        socks.remove(server)

                    else:
                    # send the message read from the socket on all other client sockets
                        for recv_sock in socks:
                            if (recv_sock != server) and (recv_sock != client):
                                recv_sock.send(msg.encode("utf-8"))
            # '''
        except KeyboardInterrupt:
            print('\b\bSession Ended...\n')

# main() executes if this file is running

if __name__ == '__main__':
    main()
