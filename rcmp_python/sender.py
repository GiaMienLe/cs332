#!/usr/bin python3
#
# Sender class that sends packets across on UDP connection
#
# author: Sean Ebenmelu
# 
# help received from Kurt W. and Darren R.

import sys, socket, os

# CONSTANTS
HOST = 'localhost'
PORT = 65432
BUFFER = 1450

class Sender:
    # Sender Constructor
    def __init__(self, destAddress=HOST, port=PORT, filename="foo.txt"):
        self.destAddress = destAddress
        self.port = port
        self.filename = filename


    # read and send file
    def readSendFile(self):
        pktID = 0
        gap_counter = 0
        pktSentSinceLastAck = 0     # counts the gap between acked packets
        acked = 1   # indicator of which packet is ACKed

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)  # times out if the ACK isn't received

        # read file into binary form and store in data var
        file = open(self.filename, 'rb')
        file_size = os.path.getsize(self.filename)
        data = file.read(BUFFER)
        marker = 0    # gets current position

        connectID = os.urandom(4) # assigns unsigned random numbers

        
        while data:

            # if current packet is to be acked, acked = 1
            if pktSentSinceLastAck == gap_counter:
                acked = 1
                print("Next packet to be ACKed: {}".format(pktID))
            else:
                acked = 0

            # Header and Components
            numOfBytes = file_size.to_bytes(4, 'big')

            header = connectID + numOfBytes + pktID.to_bytes(4, 'big') + acked.to_bytes(1, 'big')

            # SEND HEADER
            sock.sendto(header + data, (self.destAddress, self.port))
            print("Sending packet {}...".format(pktID))

            # Runs a Stop and Go Protocol
            for x in range(7):
                try:
                    if acked == 1:

                        # Wait for ACK packet
                        ackPkt, address = sock.recvfrom(8)

                        marker = file.tell()    # gets current position
                            
                        # Packet is received and colors text green   
                        print("\033[32mACK Message Len: {} bytes received\033[0m".format(len(ackPkt)))

                        gap_counter += 1
                        pktSentSinceLastAck = 0
                    break
                except socket.timeout:
                    if x == 4:
                         # Timeout Error occurs colors text red

                        print("\033[91mFile transfer success unknown.\033[0m")
                        exit(1)
                    print("Sender Timeout: No ACK was received")
                    file.seek(marker)
                    header = connectID + numOfBytes + pktID.to_bytes(4, 'big') + acked.to_bytes(1, 'big')
                    data = file.read(BUFFER)
                    sock.sendto(header + data, (self.destAddress, self.port))

            pktSentSinceLastAck += 1
            pktID += 1
            data = file.read(BUFFER) # reads next data
            print("\n")

# RUNS SENDER 
if __name__ == '__main__':
    # if cmd args are less than 2, use default Sender object
    if len(sys.argv) < 2:
        thisSender = Sender()
        thisSender.readSendFile()
        
    # if cmd args are less than 2, use default Sender object
    else:
        dest = sys.argv[1]
        portNum = int(sys.argv[2])
        a_file = sys.argv[3]
        thisSender = Sender(dest, portNum, a_file)
        thisSender.readSendFile()
