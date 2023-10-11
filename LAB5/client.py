import socket
import threading
import json
import time
import os
import base64

HOST = '127.0.0.1'
PORT = 8080
name = ''

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((HOST, PORT))
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
    message = input("Enter a message type (or 'exit' to quit):\n")

    if message.lower() == 'exit':
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
    
    else:
        print("Wrong message type!")
        return
    
    if message_json:
        data = json.dumps(message_json).encode('utf-8')
        data_length = len(data)
        client_socket.send(data_length.to_bytes(1024, byteorder='big'))
        client_socket.send(json.dumps(message_json).encode('utf-8'))


def handle_connect():
    global name
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
    if name:
        sender = name
    else:
        sender = input("Please, enter your name: ", )
        name = str(sender)
    
    room = input('Enter room name: ')
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
    path = input('Enter relative path to file: ')
    room = input('Enter your room: ')
    
    if not os.path.exists(path):
        print(f"Path {path} does not exist!")
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

def receive_messages(client_socket: socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        message = json.loads(message)
        

        if 'message' in message['payload'].keys():
            print(f"Received: {message['payload']['message']}")
        else:
            raise KeyError()

if __name__ == "__main__":
    start_client()