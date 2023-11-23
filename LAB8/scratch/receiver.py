import socket

# Create a UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
receiver_socket.bind(('0.0.0.0', 12345))

print("Waiting for broadcasts...")


def main():
    try:
        while True:
            # Receive the message
            data, address = receiver_socket.recvfrom(1024)
            print(f"Received message from {address}: '{data.decode('utf-8')}'")
    except KeyboardInterrupt:
        print("Receiver stopped.")
        receiver_socket.close()

if __name__ == "__main__":
    main()