import zmq
import threading
import time

context = None
socket = None
poller = zmq.Poller()
zmq_req_lock = threading.Lock()


def socket_register():
    global context, socket, poller, zmq_req_lock 
    context = zmq.Context()
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.LINGER, 0)
    #poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

request = 0
thread_count = 1
__videv_thread_list = []
def send_req_thread():
    global context, socket, poller, zmq_req_locki, thread_count
    print("len(__videv_thread_list): {}".format(len(__videv_thread_list)))
    while len(__videv_thread_list) > 0:
        if __videv_thread_list[0] is not None:
            if not __videv_thread_list[0].is_alive():
                __videv_thread_list.pop(0)
                print("Thread ID {}  is dead !! we are releasing Lock".format(threading.get_ident()))
                if zmq_req_lock.locked():
                    zmq_req_lock.release()
                break
            else:
                if socket == None:
                    print("Socket is not registered !!")
                    socket_register()
                    break
                if zmq_req_lock.locked():
                    time.sleep(1)
                    continue 
                else:
                    break
        else:
            __videv_thread_list.pop(0)
    print("acquiring lock !!")
    zmq_req_lock.acquire()
    print("Sending request %s …" % thread_count)
    socket.send(b"Hello")
    message = {}
    if poller.poll(6*1000):
        message = socket.recv()
        print("Received reply %s [ %s ]" % (thread_count, message))
        if not message == {}:
            zmq_req_lock.release()
        thread_count += 1
    else:
        print("Timeout processing auth request {}".format(thread_count))
        if __videv_thread_list:
            __videv_thread_list.pop(0)
        socket.close()
        context.term()
        socket_register()
        thread_count += 1
        print("socket has been re-registered for thread {} !!".format(thread_count))
        zmq_req_lock.release()
    return message


total_req = 10
while request < total_req:
    while len(__videv_thread_list) >= 8:
        time.sleep(2)
        if __videv_thread_list[0] is not None:
            if not __videv_thread_list[0].is_alive():
                __videv_thread_list.pop(0)
        else:
            __videv_thread_list.pop(0)
    if len(__videv_thread_list) < 8:
        print("Creating Thread!!")
        t = threading.Thread(target=send_req_thread, args=())
        print("Appending thread in list!!")
        __videv_thread_list.append(t)
        t.start()
    request += 1
    time.sleep(5)
