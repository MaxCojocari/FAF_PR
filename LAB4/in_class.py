import socket
import json
import re

HOST = '127.0.0.1' 
PORT = 8080 

data = json.load(open('data.json'))

def handle_request(request_data):
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    path = request_line[1]
    
    response_content = ''
    status_code = 200
    
    if path == '/':
        response_content = '<h2>Home page</h2>'
    elif path == '/about-us':
        response_content = '<h2>This is the About Us page</h2>'
    elif path == '/contacts':
        response_content = '<h2>This contacts page</h2>'
    elif path == '/products':
        response_content = handle_products_route()    
    elif re.match(r'^/products/\d$', path):
        (response_content, status_code) = handle_product_page_route(path)
    else:
        (response_content, status_code) = ('<h2>404 Not Found</h2>', 404)
    
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'

    return response

def handle_products_route():
    response_content = '<ul>'
    
    for i in range(0, len(data)):
        href = f"http://{HOST}:{PORT}/products/{i}"
        response_content += f"<li><a href={href}>{data[i]['name']}</a></li>"
    
    response_content += '</ul>'
    
    return response_content

def handle_product_page_route(path):
    i = int(path.split('products/')[1])
    
    if i >= len(data):
        return ('<h2>404 Not Found</h2>', 404)

    response_content = f'''<h1>{data[i]["name"]}</h1><h2>{data[i]["author"]}</h2><p class="price">{str(data[i]["price"])}</p><p class="description">{data[i]["description"]}</p>'''
    return (response_content, 200)

def start_server():
    # Create a socket that uses IPv4 and TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket reusability
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()     
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        response = handle_request(message)
        print(f"Received: {message}")
        client_socket.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()


