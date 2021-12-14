# zmq-REQ-REP-Poller-Multithreading
This repository explains zmq request and reply process which handles response timeout using zmq poller. We are sending request with multithreading.

# Template Output without multithreading
server has sleep of n sec for nth request from client, run server.py
```
uncanny@MSI:/mnt/d/Workspace/private_workspace/zmq-REQ-REP-Poller-Multithreading$ python3 server.py
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
Received request: b'Hello'
```
After starting the server, we can start client. In client.py, we are sending ```b"Hello"```
as request to the server. Server receives ```b"Hello"``` request and goes to sleep for n sec. for nth request, send response to client ```b"World"``` after n sec. Client has timeout of 6 sec.
```
uncanny@MSI:/mnt/d/Workspace/private_workspace/zmq-REQ-REP-Poller-Multithreading$ python3 client.py
Connecting to hello world server…
Sending request 0 …
Received reply 0 [ b'World' ]
Sending request 1 …
Received reply 1 [ b'World' ]
Sending request 2 …
Received reply 2 [ b'World' ]
Sending request 3 …
Received reply 3 [ b'World' ]
Sending request 4 …
Received reply 4 [ b'World' ]
Sending request 5 …
Received reply 5 [ b'World' ]
Sending request 6 …
Timeout processing auth request 6
Terminating socket for old request 6
socket has been re-registered for request 7
Sending request 7 …
Timeout processing auth request 7
Terminating socket for old request 7
socket has been re-registered for request 8
Sending request 8 …
Timeout processing auth request 8
Terminating socket for old request 8
socket has been re-registered for request 9
Sending request 9 …
Timeout processing auth request 9
Terminating socket for old request 9
socket has been re-registered for request 10
```
# Template Output with multithreading
- server part is same as above.
- In ```client_thread.py```,We are creating thread in each 5 sec, each thread is being processed in ```send_seq_thread```.
- In ```send_seq_thread``` function, We are handling deadlock using lock machenism.
- If thread is locked, it waits till timeout for response
- a. If timeout does'nt happen, we will get response and lock will be released. Same sockets will be used for next thread.
- b. If timeout happens, First we will remove that thread from list then we will re-register sockets and lock will be released.

```
uncanny@MSI:/mnt/d/Workspace/private_workspace/zmq-REQ-REP-Poller-Multithreading$ python3 client_thread.py
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 1
Socket is not registered !!
Connecting to hello world server…
acquiring lock !!
Sending request 1 …
Received reply 1 [ b'World' ]
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Thread ID 140099491333888  is dead !! we are releasing Lock
acquiring lock !!
Sending request 2 …
Received reply 2 [ b'World' ]
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Thread ID 140099491333888  is dead !! we are releasing Lock
acquiring lock !!
Sending request 3 …
Received reply 3 [ b'World' ]
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Thread ID 140099491333888  is dead !! we are releasing Lock
acquiring lock !!
Sending request 4 …
Received reply 4 [ b'World' ]
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Thread ID 140099491333888  is dead !! we are releasing Lock
acquiring lock !!
Sending request 5 …
Received reply 5 [ b'World' ]
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Thread ID 140099491333888  is dead !! we are releasing Lock
acquiring lock !!
Sending request 6 …
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Received reply 6 [ b'World' ]
Thread ID 140099465840384  is dead !! we are releasing Lock
acquiring lock !!
Sending request 7 …
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Timeout processing auth request 7
Connecting to hello world server…
socket has been re-registered for thread 8 !!
acquiring lock !!
Sending request 8 …
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
Timeout processing auth request 8
Connecting to hello world server…
socket has been re-registered for thread 9 !!
Creating Thread!!
Appending thread in list!!
len(__videv_thread_list): 2
acquiring lock !!
acquiring lock !!
Sending request 9 …
Timeout processing auth request 9
Connecting to hello world server…
socket has been re-registered for thread 10 !!
Sending request 10 …
Timeout processing auth request 10
Connecting to hello world server…
socket has been re-registered for thread 11 !!
```

