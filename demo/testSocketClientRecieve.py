import websocket
import sys


serverAddr = sys.argv[1]

ws = websocket.create_connection("ws://" + serverAddr + ":9001")

while True:
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)


ws.close()