from UDPConnection import UDPConnection

conn = UDPConnection("127.0.0.1", 12345, host = True, timeout = 0.5)

while True:
    val = conn.recv()
    if val == None: continue
    print("Recv:", val)
    conn.send(f"Hello {val[1]}".encode(), val[1], mark_as_responded= not val[0] == b"done")