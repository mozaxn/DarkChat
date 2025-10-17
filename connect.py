import socket

def connection_req(host, port, pub_key):

    # Create a TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the target host
        client.connect((host, port))
        print(f"Connected to {host}! Requesting for chat...")
        
        message = "CHAT:" + socket.gethostbyname(socket.gethostname())
        client.sendall(message.encode('utf-8'))
        print(f"Sent chat request to {host} on port {port}.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()
