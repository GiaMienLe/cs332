#include <iostream>
#include <fstream>

#include <vector>

#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string>
#include <arpa/inet.h>

#ifndef SENDER_H
#define SENDER_H

#define BUFFER_SIZE 1450

using namespace std;

class Sender {
    public:
        Sender();
        Sender(string destAddress, int port, string filename);
        void readFile(string filename);
        void getByteSize(string filename);
        char * readBytes(string filename);
        void printBytes(char * byteArr);
    private:
        string destAddr, file;
        int pNumber;
        char bytes[BUFFER_SIZE];
};

#endif // SENDER_H