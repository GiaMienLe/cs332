#
# Websocket-based server code. This code sends to other clients whatever
# each client sends to it. Thus, this is essentially a broadcasting service.
#
# Date: 24 June 2021
# Original author: Victor Norman at Calvin University
#
# Edited by Sean Ebenmelu
# Date: 10/13/2021

import asyncio
import websockets
import json
import socket

# Change to False when you are done debugging.
DEBUG = True
# Port the server listens on to receive connections.
PORT = 8001

# TODO: need a variable here to hold all connected clients' websocket objects.
sockets = []

def register_new_client(client_ws):
    if DEBUG:
        print('register new client!')
    # TODO: add code here to store the client_ws in your collection of websockets.
    sockets.append(client_ws)

def unregister_client(websocket):
    if DEBUG:
        print('removed new client!')
    # TODO: add code here to remove the client_ws from your collection of websockets.
    
    sockets.remove(websocket)

async def per_client_handler(client_ws, path):
    '''This function is called whenever a client connects to the server. It
    does not exit until the client ends the connection. Thus, an instance of
    this function runs for each connected client.'''
    register_new_client(client_ws)
    try:
        async for message in client_ws:
            # This next line assumes that the message we received is a stringify-ed
            # JSON object.  data will be a dictionary.
            data = json.loads(message)

            # TODO: Add the client's unique id to the message before
            # sending to everyone.
            
            # Adapted from Brian L.'s code
            data['id'] = sockets.index(client_ws)   # returns the index of client_ws and assigns to data['id']

            print('got data ', data)
            
            data['id'] = sockets.index(client_ws) # Adapted from Brian's code

            print('got data ', data)

            # TODO: Add the client's unique id to the message before
            # sending to everyone

            # TODO: Send received message to all *other* clients.
            json_data = json.dumps(data)
            for client in sockets:
                if client is not client_ws:
                    print(client)

                    await client.send(json_data)    # waits for client input

                    await client.send(json_data)

    finally:
        unregister_client(client_ws)


# Adapted from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
def getNetworkIp():
    '''This is just a way to get the IP address of interface this program is
    communicating over.'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


# Run websocket server on port PORT on the local loopback interface while you are
# still debugging your own code.
start_server = websockets.serve(per_client_handler, "localhost", PORT)

# TODO: use this next line when you are ready to deploy and test your code with others.
# (And comment out the line above.)
# start_server = websockets.serve(per_client_handler, getNetworkIp(), PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
asyncio.get_event_loop().run_forever()
