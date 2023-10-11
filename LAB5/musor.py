import uuid
import os

name, extension = os.path.splitext("myfile.jpg")
generated_uuid = uuid.uuid1()
path = "server_media/" + "general" + "/" + name + "_" + str(generated_uuid) + extension
print(path)