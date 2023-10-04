import socket

HOST = '127.0.0.1'
PORT = 8080

def send_http_request(path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Send an HTTP GET request
    request = f"GET {path} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.sendall(request.encode('utf-8'))

    # Receive and print the response from the server
    response = client_socket.recv(1024).decode('utf-8')
    print(response)

    client_socket.close()

if __name__ == "__main__":
    path = '/products'
    send_http_request(path)
