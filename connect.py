import socket
import hashlib

def connection_req(host, port, pub_key):

    # Create a TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the target host
        client.connect((host, port))
        print(f"Connected to {host}! Requesting for chat...")

        # Send a message
        sha256 = hashlib.sha256()
        sha256.update(pub_key.encode('utf-8'))
        hashed_pub_key = sha256.hexdigest()
        
        message = hashed_pub_key
        client.sendall(message.encode('utf-8'))
        print(f"Sent public key hash: {hashed_pub_key}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()
