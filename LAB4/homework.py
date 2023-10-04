import os
import socket
import shutil
import re
import json
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse

HOST = '127.0.0.1'
PORT = 8080
PAGES_DIR = "pages"
DATA_STORE = "data_homework.json"

def send_http_request(path):
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((HOST, PORT))
    
    # Send an HTTP GET request
    request = f"GET {path} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
    client_socket.sendall(request.encode('utf-8'))

    # Receive the response from the server
    response = client_socket.recv(1024).decode('utf-8')
        
    # Split the response at the double newline to separate headers and HTML content
    html_content = response.split('\n\n')[1]
    
    return html_content

def write_html_content(html_content, url_path):
    split_tokens = url_path.split('/')

    file_name = ''
    if len(split_tokens) == 2:
        file_name = split_tokens[1]
        if not file_name:
            file_name = 'home'
    elif len(split_tokens) == 3:
        file_name = split_tokens[1] + "_" + split_tokens[2]
    
    if not os.path.exists(PAGES_DIR):
        os.makedirs(PAGES_DIR)

    file_path = os.path.join(PAGES_DIR, f"{file_name}.html")
    
    with open(file_path, 'w') as file:
        file.write(html_content)

def parse_product_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    product = {
        "name": soup.find('h1').text,
        "author": soup.find('h2').text,
        "price": float(soup.find('p', class_="price").text),
        "description": soup.find('p', class_="description").text
    }
    append_to_json_file(product)

def append_to_json_file(data_dict):
    try:
        with open(DATA_STORE, "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data_dict)

    with open(DATA_STORE, "w") as file:
        json.dump(existing_data, file, indent=4)


if __name__ == "__main__":
    if os.path.exists(PAGES_DIR):
        shutil.rmtree(PAGES_DIR)
    if os.path.exists(DATA_STORE):
        os.remove(DATA_STORE)

    paths = ["/", "/about-us", "/contacts", "/products"]
    queue = deque(paths)
    seen = set()

    while queue:
        path = queue.pop()
        html = send_http_request(path)
        write_html_content(html, path)
        soup = BeautifulSoup(html, 'html.parser')

        if re.match(r'^/products/\d+$', path):
            parse_product_page(html);
        
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href not in seen:
                new_path = urlparse(href).path
                queue.append(new_path)
                seen.add(new_path)