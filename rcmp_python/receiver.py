import sys, socket

HOST = 'localhost'
PORT = 65432

class Receiver:
    def __init__(self, port=0, filename=''):
        self.port = port
        self.filename = filename
    
    # TODO: Open a FileOutputStream
    def writeBytes(self, byteArray):
        with open(self.filename, "w") as file:
            for stuff in byteArray:
                file.write(stuff)

    def run(self):
        receiveBytes = []

        # Open the socket on the given port.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', self.port))
            message, address = sock.recvfrom(PORT)

            packetSize = int (message.decode('utf-8'))
            counter = 0
            # print(i)
            while True:
                message, address = sock.recvfrom(PORT)
                receiveBytes.append(message)

                counter += 1
                if counter == packetSize:
                    break

        # input bytes into recieveBytes []
        temp = []
        for bytStuff in receiveBytes:
            temp.append(bytStuff.decode())

        receiveBytes = temp
        del temp

        writeBytes(receiveBytes)

        result = ''.join(receiveBytes)
        # print(result)

thisReceiver = Receiver(PORT, 'foo2.txt')
thisReceiver.run()
