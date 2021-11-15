#include <iostream>
#include <fstream>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include "sender.h"



using namespace std;


int main(int argc, char *argv[]){ 

    for(int i = 0; i < argc; i++){
        cout << argv[i] << "\n" << flush;
    }

    printf("\n============================\n");

    if (argc < 2){
        Sender thisSender = Sender();
    } else {
        Sender thisSender = Sender(argv[1], stoi(argv[2]), argv[3]);
    }

    // TODO: Use InetAddress.getByName() to convert the destAddress name to an InetAddress.

    // TODO: Open a datagram socket.
    int sock = socket(AF_INET, SOCK_DGRAM, 0);

    

    // TODO: Create a new DatagramPacket with those bytes and send it.

    // TODO: Close the socket.
    // close(sock);

    cout << "\n\n---EOF---" << endl;
}