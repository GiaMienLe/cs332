import sys, socket, os

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
def readSendFile(filename):
    pktID, STARTID = 0, 0
    gap_counter, gap = 0, 0
    ackedID = 0
    is_acked = 1 # (to ack) 0 (not to ack)    

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # read file into binary form and store in data var
    file = open(filename, 'rb')

    try:
        while True:
            # GAP CALCULATION
            if pktID == ackedID:
                is_acked = 1 
            else:
                is_acked = 0

            print("PACKET to be ACKed: {}".format(ackedID))

            data = file.read(BUFFER)

            if len(data) == 0:
                break

            # Header and Components
            connectID = os.urandom(4) # assigns unsigned random numbers
            numOfBytes = len(data).to_bytes(4, 'big')

            if pktID == 0:
                is_acked = 1 
            header = connectID + numOfBytes + pktID.to_bytes(4, 'big') + is_acked.to_bytes(1, 'big')
            print("Sending packet with size of: {}".format(len(header + data)))

            # SEND HEADER
            sock.sendto(header + data, (HOST, PORT))
            sock.settimeout(5)

            # Wait for ACK packet
            ackPkt, address = sock.recvfrom(8)
            print("ACK Message Len: {} bytes received from -- {}".format(len(ackPkt), address))

            pktID += 1
            gap = abs(STARTID - pktID)
            ackedID += gap


    except KeyboardInterrupt:
        print("\b\b\n-------------------------")
        file.close()
        sock.close()

# if cmd args are less than 2, use default Sender object
if len(sys.argv) < 2:
    thisSender = Sender()
    readSendFile(thisSender.filename)
else:
    dest = sys.argv[1]
    portNum = int(sys.argv[2])
    a_file = sys.argv[3]
    thisSender = Sender(dest, portNum, a_file)
    readSendFile(a_file)
