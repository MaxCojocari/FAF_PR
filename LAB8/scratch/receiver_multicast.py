import socket

# Multicast group address and port
multicast_group = '224.0.0.1'
multicast_port = 12345

# Create a UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the multicast group address and port
receiver_socket.bind((multicast_group, multicast_port))

# Join the multicast group
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))

print(f"Waiting for multicasts on {multicast_group}:{multicast_port}...")

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
