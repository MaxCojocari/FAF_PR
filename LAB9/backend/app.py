from flask import Flask, request
from flask_cors import CORS
from service import MailService
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

mail_service = MailService(
    os.getenv('EMAIL_SENDER'), 
    os.getenv('APP_PASSWORD'), 
    os.getenv('FTP_SERVER'),
    os.getenv('FTP_USERNAME'), 
    os.getenv('FTP_PASSWORD')
)

@app.route('/api/email', methods=['POST'])
def send_email_to_recipients():
    try:
        data = request.get_json()
        mail_service.send_email(data["subject"], data["body"], data["recipients"])
        return {"message": "Email sent successfully!"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
@app.route('/api/email/attachment', methods=['POST'])
def upload_file():
    try:
        if "file" not in request.files:
            return {"message": "No file part in the request"}, 400

        file = request.files['file']

        if file.filename == '':
            return {"message": "No selected file"}, 400

        link = mail_service.upload_file(file)
        
        return {"ftp-link": link}, 200
        
    except Exception as e:
        return {"error": str(e)}, 500  

@app.route('/api/email/attachment', methods=['GET'])
def download_file():
    try:
        data = request.get_json()
        mail_service.download_file(data["file_name"])
        return {"message": "File downloaded successfully!"}, 200
        
    except Exception as e:
        return {"error": str(e)}, 500  

app.run() 