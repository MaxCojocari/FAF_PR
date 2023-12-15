import smtplib
from email.mime.text import MIMEText
from ftplib import FTP

class MailService():
    def __init__(self, sender, email_password, ftp_server, ftp_username, ftp_passwd) -> None:
        self.sender = sender
        self.emailpassword = email_password
        self.smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.smtp_server.login(self.sender, self.emailpassword)
        self.ftp = FTP(ftp_server)
        self.ftp.login(user=ftp_username, passwd=ftp_passwd)

    def send_email(self, subject, body, recipients):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)
        self.smtp_server.sendmail(self.sender, recipients, msg.as_string())

    def upload_file(self, file):
        file_name = file.filename.replace(" ", "_")
        remote_file_path = 'faf213/MaxCojocari/' + file_name
        self.ftp.storbinary(f'STOR {remote_file_path}', file)
        return f"ftp://yourusername:yourusername@138.68.98.108/faf213/MaxCojocari/{file_name}"
    
    def download_file(self, file_name):        
        with open(f"uploaded_files/{file_name}", "wb") as file:
            self.ftp.retrbinary(f"RETR faf213/MaxCojocari/{file_name}", file.write)
