#!/usr/bin python3
#
# Receiver class that receives packets from sender on UDP connection
#
# author: Sean Ebenmelu
# 
# help received from Kurt W. and Darren R.

import sys, socket

# CONSTANTS
HOST = 'localhost'
PORT = 65432
BUFFER = 1450

class Receiver:
    # Receiver Constructor
    def __init__(self, port, filename):
        self.port = port
        self.filename = filename
    
    # Run receiver
    def run(self):

        # write to a file what is received from sender
        file = open(self.filename, 'wb')

        # Open a datagram socket on the given port.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', PORT)) # bind to socket

        while True:
            message, address = sock.recvfrom(BUFFER + 13)
            sock.settimeout(2)

            try:
                if message:
                    file.write(message[13:])

                    connectID = message[:4] 
                    pktID = message[8:12]
                    ackPkt = connectID + pktID

                    pktID = int.from_bytes(pktID, 'big')

                    # Packet is received and colors text green 
                    print("\033[32mPacket {} received\033[0m".format(pktID))

                # sends an ACK
                    sock.sendto(ackPkt, address)

                    if len(message) != (BUFFER + 13):
                        break
            except KeyboardInterrupt:
                print("Receiver closed")
                exit(1)
        file.close()
        sock.close()

# RUNS RECEIVER
if __name__ == '__main__':
    if len(sys.argv) < 2:
        thisReceiver = Receiver(PORT, 'foo2.txt')
        thisReceiver.run()
    else:
        thisReceiver = Receiver(sys.argv[1], sys.argv[2])
        thisReceiver.run()