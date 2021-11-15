#include <iostream>
#include <stdio.h>
#include <sys/socket.h>

#define SIZE 1024
#define IP_PROTOCOL 0
#define PORT_NUM 8080

using namespace std;

int main(int argc, char *argv[]){ 
    for(int i = 0; i < argc; i++){
        cout << argv[i] << "\n" << flush;
    }

    cout << "---EOF---" << endl;
}