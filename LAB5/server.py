import socket
import threading
import json
import base64
import os
import uuid

HOST = '127.0.0.1'
PORT = 8080

clients = []
rooms = {}
uuids = {}

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    
    while True:
        message = receive_message(client_socket)
        
        print(f"Received from {client_address}: {message}")

        if message["type"] == "connect":
            handle_connect_request(message, client_socket, client_address)

        if message["type"] == "message":
            handle_message_request(message, client_socket, client_address)
        
        if message["type"] == "upload":
            handle_upload_request(message, client_socket, client_address)

    client_socket.close()

def handle_connect_request(message, client_socket, client_address):
    if message["payload"]["room"] not in rooms.keys():
        rooms[message["payload"]["room"]] = []
    
    rooms[message["payload"]["room"]].append(
        {
            "name": message["payload"]["name"], 
            "socket": client_socket, 
            "address": client_address
        }
    )
    
    message_json = {
        "type": "connect_ack",
        "payload": {
            "message": f"Connected to the '{message['payload']['room']}' room."
        }
    }
    
    send_response_message(message_json, client_socket)
    # client_socket.send(json.dumps(message_json).encode('utf-8'))

    notification_message_json = {
        "type": "notification",
        "payload": {
            "message": f"{message['payload']['name']} has joined the room."
        }
    }

    for member in rooms[message["payload"]["room"]]:
        if member["address"] != client_address:
            send_response_message(notification_message_json, member["socket"])
            # member["socket"].send(json.dumps(notification_message_json).encode('utf-8'))

def handle_message_request(message, client_socket, client_address):
    if not message["payload"]["room"] in rooms.keys():
        err_message = {
            'payload': {
                'message': f"'{message['payload']['room']}' room does not exist!"
            }
        }
        send_response_message(err_message, client_socket)
        # client_socket.send(json.dumps(err_message).encode('utf-8'))
        return 
    
    chat_members = rooms[message["payload"]["room"]]
    if not is_member_exist(client_address, chat_members):
        err_message = {
            'payload': {
                'message': f"User {message['payload']['sender']} does not exist in this room!"
            }
        }
        send_response_message(err_message, client_socket)
        # client_socket.send(json.dumps(err_message).encode('utf-8'))
        return

    new_msg = {
        'payload': {
            'message': f"{message['payload']['sender']}: {message['payload']['text']}"
        }
    }
    for member in chat_members:
        if member["address"] != client_address:
            send_response_message(new_msg, member["socket"])
            # member["socket"].send(json.dumps(new_msg).encode('utf-8'))

def handle_upload_request(message, client_socket, client_address):
    # Check if room exists
    if not message["payload"]["room"] in rooms.keys():
        err_message = {
            'type': 'error',
            'payload': {
                'message': f"'{message['payload']['room']}' room does not exist!"
            }
        }
        send_response_message(err_message, client_socket)
        # client_socket.send(json.dumps(err_message).encode('utf-8'))
        return
    
    # Check if user exists in chat room
    chat_members = rooms[message["payload"]["room"]]
    if not is_member_exist(client_address, chat_members):
        err_message = {
            'type': 'error',
            'payload': {
                'message': f"User {message['payload']['sender']} does not exist in this room!"
            }
        }
        send_response_message(err_message, client_socket)
        # client_socket.send(json.dumps(err_message).encode('utf-8'))
        return

    # Convert receied bytes into suitable file format
    decoded_bytes = base64.b64decode(message["payload"]["data"])

    if message["payload"]["room"] not in uuids.keys():
        uuids[message["payload"]["room"]] = {}
    if client_address not in uuids[message["payload"]["room"]].keys():
        generated_uuid = str(uuid.uuid1())
        uuids[message["payload"]["room"]][client_address] = generated_uuid
    
    user_uuid = uuids[message["payload"]["room"]][client_address]
    
    path = "server_media/" + message["payload"]["room"] + "/" + user_uuid 

    if not os.path.exists(path):
        os.makedirs(path)
    
    path = path + "/" + message["payload"]["file_name"]

    # Save in the specified directory
    with open(path, 'wb') as f:
        f.write(decoded_bytes)

    sender_name = get_sender_name(message, client_address);
    new_msg = {
        'type': 'upload_ack',
        'payload': {
            'message': f"User {sender_name} uploaded {message['payload']['file_name']} file"
        }
    }
    chat_members = rooms[message["payload"]["room"]]
    
    for member in chat_members:
        if member["address"] != client_address:
            send_response_message(new_msg, member["socket"])
            # member["socket"].send(json.dumps(new_msg).encode('utf-8'))

def handle_download_request(message, client_socket, client_address):
    path = get_file(message["payload"]["file_name"])
    
    if not path:
        err_message = {
            'type': 'error',
            'payload': {
                'message': f"'{message['payload']['file_name']}' does not exist!"
            }
        }
        send_response_message(err_message, client_socket)
        # client_socket.send(json.dumps(err_message).encode('utf-8'))
        return
    
    with open(path, 'rb') as file:
        file_bytes = file.read()

    encoded_data = base64.b64encode(file_bytes).decode('utf-8')

    message_json = {
        "type": "download_ack",
        "payload": {
            "file_name": os.path.basename(path),
            "data": encoded_data
        }
    }

    send_response_message(message_json, client_socket)

def receive_message(client_socket):
    if not client_socket:
        return {}
    
    length_header = client_socket.recv(1024)
    if not length_header:
        return None
    message_length = int.from_bytes(length_header, byteorder='big')

    full_data = b""

    while len(full_data) < message_length:
        data = client_socket.recv(1024)
        full_data += data

    return json.loads(full_data.decode('utf-8'))

def is_member_exist(client_address, members):
    return any(member.get('address') == client_address for member in members)

def get_sender_name(message, client_address):
    members = rooms[message["payload"]["room"]]
    for member in members:
        if member["address"] == client_address:
            return member["name"]
    return ""

def send_response_message(msg, client_socket):
    data = json.dumps(msg).encode('utf-8')
    data_length = len(data)
    client_socket.send(data_length.to_bytes(1024, byteorder='big'))
    client_socket.send(json.dumps(msg).encode('utf-8'))

if __name__ == "__main__":
    start_server()