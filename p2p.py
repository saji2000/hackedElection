import socket
import pickle
import getpass
import os.path
import random
import time
import threading
import select
#from flask import Flask
#app = Flask(__name__)


global_out = ""
global_in = []

def connection(c, addr):
    global global_out
    OldOutMsg = ""
    OldTime = time.time()
    print("Created thread")
    while True:
        c.setblocking(0)
        try:
            in_msg = c.recv()
        except:
            in_msg=""
        if in_msg == "DC":
            break
        elif in_msg != "":
            print("msg")
            print(in_msg)
            #global_in.append({addr:in_msg})
            OldTime = time.time()
        if global_out != OldOutMsg:
            print("printed")
            c.send(bytes(global_out,'utf-8'))

            OldOutMsg = global_out
        if time.time()-OldTime >= 15:
            break
    print("disconnecting from", addr)
    c.close()

def connect(ip,port=80):
    try: # ipv4 over tcp
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print ("socket creation failed with error", err)

    try:
        s.connect((ip,port))
        print("connected to", ip)
        threading.Thread(target=connection, args=(s, ip,))
        return True
    except:
        print("unable to connect to", ip)
        return False


def listen(port = 80):
    s = socket.socket()

    s.bind(('',port))

    s.listen(5) # 5 is queue size
    try:
        s.settimeout(0.25)
        c, addr = s.accept()
        print("connected to", addr)
        threading.Thread(target=connection, args=(c, addr,)).start()


    except socket.timeout as err:
        pass

def broadcast(msg):
    print("broadcasting")
    global global_out
    global_out = msg


if __name__ == "__main__":

    start = time.time()
    user = getpass.getuser()
    location = 'C:/Users/' + user + "/nodes.p"
    if not os.path.isfile(location):
        nodes = {"127.0.0.1"}
        file = open(location, "wb")
        pickle.dump(nodes,file)
    file = open(location, "rb")
    nodes = pickle.load(file)
    nodes = {"127.0.0.1"}
    max_peers = 10
    peers = set()
    connected = set()
    i = random.sample(nodes,1)[0]

    if i is not None:
        count = 1
    else:
        count = 0

    while count <= len(nodes) and len(peers)<=max_peers:
        peers.add(i)
        count += 1
        try:
            i = random.sample(nodes-peers,1)[0]
        except:
            pass

    while True:
        listen()
        if len(peers)>0 and len(peers)<=max_peers:
            for i in nodes-peers:
                if i is not None:
                    success = connect(i, 80)
                    if success:
                        connected.add(i)
            for i in connected:
                peers.remove(i)
        print(threading.active_count())

        msg = "hello peeps"
        threading.Thread(target=broadcast,args=(msg,)).start()
