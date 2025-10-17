import socket

def broadcaster(stop_event, port, pub_key):
    BCAST_IP = "255.255.255.255"
    INTERVAL = 2.0  # seconds

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        while not stop_event.is_set():
            message = bytes("DarkChat:" + socket.gethostbyname(socket.gethostname()) + ":" + pub_key, "utf-8")
            sock.sendto(message, (BCAST_IP, port))
            
            # wait either INTERVAL or until stop_event is set
            stop_event.wait(INTERVAL)
    finally:
        sock.close()