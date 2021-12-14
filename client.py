import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.LINGER, 0)
# use poll for timeouts:
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    socket.send(b"Hello")
    '''
    We have set response timeout of 6 sec.
    '''
    if poller.poll(6*1000):
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))
    else:
        print("Timeout processing auth request {}".format(request))
        print("Terminating socket for old request {}".format(request))
        socket.close()
        context.term()
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.setsockopt(zmq.LINGER, 0)
        poller.register(socket, zmq.POLLIN)
        print("socket has been re-registered for request {}".format(request+1))
