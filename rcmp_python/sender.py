import sys, socket

byteArr = []

HOST = 'localhost'
PORT = 65432

class Sender:
    def __init__(self, destAddress="", port=0, filename=""):
        self.destAddress = destAddress
        self.port = port
        self.filename = filename

    # Figure out how to read the file contents into a byte[]

    def readFile(self, filename):
        # print("\nFile Read: ")
        packetLimit = 1450
        counter = 0
        with open(filename, "r") as file:
            # TODO: find a more efficient way of doing this
            for line in file:
                for c in line:
                    if counter < packetLimit:
                        byteArr.append(bytes(c.encode()))
                        counter += 1
                    else:
                        # self.sendBytes()
                        # byteArr.clear()     # clear packet
                        # counter = 0         # reset count, 
                        pass
        # print byteArr
        # for c in byteArr:
        #     print(c)

    def getByteArr(self):
        return byteArr

    def sendBytes(self):
        # Open a datagram socket and handles sock.close().

        # with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        #     packetSize = str(len(self.getByteArr()))    # will be given to receiver to stop server

        #     sock.sendto(bytes(packetSize.encode()), (HOST, PORT))

        #     for bStuff in self.getByteArr():
        #         sock.sendto(bStuff, (HOST, PORT))

        pass

print(str(sys.argv))

if len(sys.argv) < 2:
    thisSender = Sender()
else:
    dest = sys.argv[1]
    portNum = int(sys.argv[2])
    a_file = sys.argv[3]
    thisSender = Sender(dest, portNum, a_file)

# Use socket.getByName() to convert the destAddress IP Address.
ip_addr = socket.gethostbyname(HOST)
print(ip_addr)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    packetSize = str(len(thisSender.getByteArr()))    # will be given to receiver to stop server

    sock.sendto(bytes(packetSize.encode()), (HOST, PORT))

    for bStuff in thisSender.getByteArr():
        sock.sendto(bStuff, (HOST, PORT))