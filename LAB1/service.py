import requests

# post
someObject = {"msg": "Hello"}
data = requests.post("http://127.0.0.1:5000/hello", json=someObject)

print(data.text)
