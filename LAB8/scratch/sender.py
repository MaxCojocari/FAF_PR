import socket
import time

# Create a UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Broadcast address and port
broadcast_address = ('<broadcast>', 12345)

# Message to be broadcasted
message = "Hello, broadcast world!"

def main():
    try:
        while True:
            # Send the message
            sender_socket.sendto(message.encode('utf-8'), broadcast_address)
            print(f"Sent: '{message}' to {broadcast_address}")
            time.sleep(2)

    except KeyboardInterrupt:
        print("Broadcast stopped.")
        sender_socket.close()


if __name__ == "__main__":
    main()