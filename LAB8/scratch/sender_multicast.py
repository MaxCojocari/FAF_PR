import socket
import time

# Multicast group address and port
multicast_group = '224.0.0.1'
multicast_port = 12345
multicast_address = (multicast_group, multicast_port)

# Message to be multicast
message = "Hello, multicast world!"

# Create a UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the time-to-live (TTL) for the multicast message
sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

def main():
    # Message to be multicast
    i = 0
    try:
        while True:
            message = f"{i} Hello, multicast world!"
            # Send the message
            sender_socket.sendto(message.encode('utf-8'), multicast_address)
            print(f"Sent: '{message}' to {multicast_group}:{multicast_port}")
            time.sleep(2)
            i += 1

    except KeyboardInterrupt:
        print("Multicast stopped.")
        sender_socket.close()


if __name__ == "__main__":
    main()