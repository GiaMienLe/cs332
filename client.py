"""
    !/bash/python3/

    A chat client

    SITES USED:
        https://stackoverflow.com/questions/34984443/using-select-method-for-client-server-chat-in-python
        https://www.tutorialspoint.com/simple-chat-room-using-python
        https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
        https://realpython.com/python-sockets/#echo-client
        https://pymotw.com/2/socket/tcp.html
        https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
        https://docs.python.org/3/howto/sockets.html


    Sean Ebenmelu (sce22)
    09/20/2021
"""

import select, curses, argparse, socket, sys, random

# USERCOLOR = random.randint(1,256)      attempted to use curses


# tutorialspoint
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # creating a new socket object
host_name = socket.gethostname()    # maroon07

# soc.bing((host_name, port))

"""     ARGS SETUP      """
parser = argparse.ArgumentParser(description="A prattle client")

parser.add_argument("-n", "--name", dest="name", help="name to be prepended in messages (default: machine name)")
parser.add_argument("-s", "--server", dest="server", default="127.0.0.1",
                    help="server hostname or IP address (default: 127.0.0.1)")
parser.add_argument("-p", "--port", dest="port", type=int, default=12345,
                    help="TCP port the server is listening on (default 12345)")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                    help="turn verbose output on")
args = parser.parse_args()

def runChatClient():

    server = args.server    # ip address of server
    port = args.port        # port number of server
    sender = args.name      # your username

    soc.connect((server, port)) # connects to server

    data = soc.recv(1024)       # handles welcome to server message
    print(data.decode())        # prints message from server


    # https://stackoverflow.com/questions/34984443/using-select-method-for-client-server-chat-in-python

    socket_list = [sys.stdin, soc]  # holds list of sockets connected

    """
        Controls the sending and receiving of messages
    """
    def messageProcess():
        try:
            readWhen, write, exception = select.select(socket_list, [], []) # holds a queue of an array of sockets, exceptions, and waiting messages

            for sockets in readWhen:
                if sockets == soc:          # if socket is current socket, receive incoming message, if empty connection is lost
                    data = soc.recv(2048)
                    if data == b'':
                        raise RuntimeError
                    else:
                        print('{}'.format(data.decode()))   # decodes and prints incoming message
                else:                           # else send message from other user to server
                    msg = sys.stdin.readline()
                    msg = sender + ' says: ' + msg
                    soc.send(msg.encode())  # encodes message
        except RuntimeError:
            print('Connection lost.....')
            sys.exit(0)

    while True:
        try:
            messageProcess()
        except RuntimeError:
            print('Connection lost.....')
            soc.close()
            sys.exit(0)
        except KeyboardInterrupt:

            # https://stackoverflow.com/questions/27260751/python-hide-c-from-sigint
            print('\nSession ended')
            print("\b\b\r_________________________")
            soc.close()
            sys.exit(0)

# if this file is running
if __name__ == "__main__":
    runChatClient()
