import websocket
import sys

serverAddr = sys.argv[1]

ws = websocket.create_connection("ws://" + serverAddr + ":9001")

while True:
    val = input("Enter your value: ") 
    ws.send(val)


ws.close()
