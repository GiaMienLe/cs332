#include <iostream>
#include <sys/socket.h>

using namespace std;

int main(){
    int sock = socket(AF_INET, SOCK_DGRAM, 0);

    int PORT = 12345;
    // cin >> PORT;    // get port number
}