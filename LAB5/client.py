import socket
import threading
import json
import time
import os
import base64
import uuid
import shutil

HOST = '127.0.0.1'
PORT = 8080
DOWNLOAD_DIR = str(uuid.uuid1())
BUFFER_SIZE = 1024

name = ''
room = ''

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((HOST, PORT))

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    print(f"Connected to {HOST}:{PORT}")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        time.sleep(0.1)
        handle_input_message(client_socket)
    
    client_socket.close()

def handle_input_message(client_socket: socket):
    global name
    message = input("Enter message type (or 'exit' to quit):\n")

    if message.lower() == 'exit':
        if os.path.exists(DOWNLOAD_DIR):
            shutil.rmtree(DOWNLOAD_DIR)
        exit()
        return
    
    elif not message.lower():
        return

    elif message.lower() == 'connect':
        message_json = handle_connect()

    elif message.lower() == 'disconnect':
        message_json = handle_disconnect()

    elif message.lower() == 'message':
        message_json = handle_message()

    elif message.lower() == 'upload':
        message_json = handle_upload()

    elif message.lower() == 'download':
        message_json = handle_download()
    
    else:
        print("Wrong message type!")
        return
    
    if message_json:
        data = json.dumps(message_json).encode('utf-8')
        data_length = len(data)
        client_socket.send(data_length.to_bytes(BUFFER_SIZE, byteorder='big'))
        client_socket.send(json.dumps(message_json).encode('utf-8'))


def handle_connect():
    global name
    global room

    room = input('Enter room name: ')
    if not name:
        name = input('Enter your name: ')

    return {
        "type": "connect",
        "payload": {
            "name": name,
            "room": room
        }
    }

def handle_disconnect():
    room = input('Enter room name to disconnect: ')

    return {
        "type": "disconnect",
        "payload": {
            "name": name,
            "room": room
        }
    }

def handle_message():
    global name
    global room

    if name:
        sender = name
    else:
        sender = input("Please, enter your name: ", )
        name = str(sender)
    
    text = input('Enter message: ')

    return {
        "type": "message",
        "payload": {
            "sender": sender,
            "room": room,
            "text": text
        }
    }

def handle_upload():
    global room
    path = input('Enter relative path to file: ')
    
    if not os.path.exists(path):
        print(f"File {os.path.basename(path)} does not exist!")
        return 
    
    with open(path, 'rb') as file:
        file_bytes = file.read()

    encoded_data = base64.b64encode(file_bytes).decode('utf-8')

    return {
        "type": "upload",
        "payload": {
            "room": room,
            "file_name": os.path.basename(path),
            "data": encoded_data
        }
    }

def handle_download():
    global room
    file_name = input('Enter name of file to download: ')

    return {
        "type": "download",
        "payload": {
            "room": room,
            "file_name": file_name,
        }
    }

def receive_messages(client_socket):    
    while True:
        length_header = client_socket.recv(BUFFER_SIZE)
        message_length = int.from_bytes(length_header, byteorder='big')

        full_data = b""

        while len(full_data) < message_length:
            data = client_socket.recv(BUFFER_SIZE)
            full_data += data

        message = json.loads(full_data.decode('utf-8'))      
        
        if 'type' in message.keys():
            if message['type'] == "download_ack":
                decoded_bytes = base64.b64decode(message["payload"]["data"])
                path = os.path.join(DOWNLOAD_DIR, message['payload']['file_name'])
                with open(path, 'wb') as f:
                    f.write(decoded_bytes)
                continue

        if 'message' in message['payload'].keys():
            print(message['payload']['message'])


if __name__ == "__main__":
    start_client()