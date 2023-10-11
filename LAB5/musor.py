import os
import json
import base64

path = "folder/subfolder/car.jpg"

# if os.path.exists(path):
#     print(f"{path} exists in the current directory.")
# else:
#     print(f"{path} does not exist in the current directory.")
file_data = ''

with open(path, 'rb') as f:
    file_data = f.read()

# message_json = {
#     "name": os.path.basename(path),
#     "data": file_data
# }
# print(json.dumps(message_json))

# Read the file in binary mode
with open(path, 'rb') as file:
    file_bytes = file.read()

encoded_string = base64.b64encode(file_bytes).decode('utf-8')

decoded_bytes = base64.b64decode(encoded_string)

# Optionally, write the bytes back to a file
with open('new_car.jpg', 'wb') as file:
    file.write(decoded_bytes)