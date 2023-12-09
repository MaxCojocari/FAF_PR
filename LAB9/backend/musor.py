# ftp_path="max/user/file.txt"
# path_tokens = ftp_path.split('/')
# print(path_tokens[-1])

from ftplib import FTP
ftp = FTP('138.68.98.108')
ftp.login(user='yourusername', passwd='yourusername')
# ftp.delete('faf213/MaxCojocari/bostan.jpg')

# ftp.cwd('faf213/MaxCojocari')
# file_list = ftp.nlst()
# print("List of files:", file_list)

# ftp.mkd("faf213/MaxCojocari")

# with open('uploaded_files/bostan.jpg', 'rb') as local_file:
#     ftp.storbinary('STOR faf213/MaxCojocari/bostan.jpg', local_file)

with open('uploaded_files/bostan.jpg', 'wb') as local_file:
    ftp.retrbinary('RETR faf213/MaxCojocari/bostan.jpg', local_file.write)