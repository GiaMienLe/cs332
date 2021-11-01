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
            message, address = sock.recvfrom(BUFFER + 13)
            sock.settimeout(2)

            if message:
                file.write(message[13:])

                connectID = message[:4] 
                pktID = message[8:12]
                ackPkt = connectID + pktID
                is_acked = message[12]
                print(is_acked)

            # sends an ACK
                sock.sendto(ackPkt, address)

                if len(message) != (BUFFER + 13):
                    break
        file.close()
        sock.close()

thisReceiver = Receiver(PORT, 'foo2.txt')
thisReceiver.run()
