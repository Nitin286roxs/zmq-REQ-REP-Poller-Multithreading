import time
import zmq

context = zmq.Context()
#socket = context.socket(zmq.PULL)
socket = context.socket(zmq.REP)

socket.bind("tcp://*:5555")
#socket.RCVTIMEO = 6000
i = 0 
while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)
    #Get the reply.
    time.sleep(i)
    i+=1
    #  Send reply back to client
    socket.send(b"World")
