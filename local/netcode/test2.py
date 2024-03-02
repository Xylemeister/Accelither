from UDPConnection import UDPConnection

conn = UDPConnection("127.0.0.1", 12345, timeout = 0.5)

a = 0

from time import sleep

while True:
    a += 1
    if a < 10:
        conn.send("Hello2".encode(), mark_as_responded = False)
    else:
        conn.send("done".encode(), mark_as_responded = False)
    val = conn.recv(will_respond = False)
    print("Recv:", val)
    sleep(1)