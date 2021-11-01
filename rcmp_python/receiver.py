import sys, socket

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
        sock.bind((HOST, PORT)) # bind to socket

        while True:
            message, address = sock.recvfrom(BUFFER + 12)
            sock.settimeout(2)

            if message:
                print(message)
                file.write(message[12:])

                connectID = message[:4] 
                pktID = message[8:12]
                ackPkt = connectID + pktID

            # sends an ACK
                sock.sendto(ackPkt, address)

                if len(message) != (BUFFER + 12):
                    break
        file.close()
        sock.close()

thisReceiver = Receiver(PORT, 'foo2.txt')
thisReceiver.run()
