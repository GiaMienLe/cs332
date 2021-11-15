#include "sender.h"
#define SIZE 1024
#define IP_PROTOCOL 0
#define PORT_NUM 8080

Sender::Sender(){
    destAddr = "127.0.0.1";
    pNumber = 80;
    file = "foo.txt";

    readFile(file);
    getByteSize(file);
    readBytes(file);
    printBytes(readBytes(file));
}

Sender::Sender(string destAddress, int port, string filename){
    destAddr = destAddress;
    pNumber = port;
    file = filename;

    readFile(file);
    getByteSize(file);
}

void Sender::readFile(string filename){
    string line;
    ifstream myfile (filename);

    if (myfile.is_open()){
        while (getline(myfile, line)){
            cout << line << '\n';
        }
        myfile.close();
    }   
    else {
        cout << "Unable to open file";
    }
}

void Sender::getByteSize(string filename){
    streampos begin, end;
    ifstream myfile (filename, ios::binary);
    begin = myfile.tellg();
    myfile.seekg (0, ios::end);
    end = myfile.tellg();

    cout << "size is: " << (end-begin) << " bytes.\n";
}

char * Sender::readBytes(string filename){
    char file_bytes [BUFFER_SIZE] = {' '};
    int i = 0;
    char byte = 0;
    
    ifstream myfile (filename);

    if (myfile.is_open()){
        while (myfile.get(byte)){
            file_bytes[i] = byte;
            i++;
        }
        myfile.close();
    }   
    else {
        cout << "Unable to open file";
    }

    return file_bytes;
}

void Sender::printBytes(char[] byteArr){
    // prints out the bytes taken
    for (const auto &n : byteArr) {
        cout << n << "-";
    }
}