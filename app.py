import os
from flask import Flask
from flask_cors import CORS

from controller.bca_controller import bca_controller
from controller.bri_controller import bri_controller

from waitress import serve


app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Batas ukuran file hingga 16 MB

UPLOAD_FOLDER = 'uploads/'
EXTRACT_FOLDER = 'extracted_data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(EXTRACT_FOLDER):
    os.makedirs(EXTRACT_FOLDER, exist_ok=True)
    
if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    #We now use this syntax to server our app. 
    serve(app, host='0.0.0.0', port=5000)

@app.route('/', methods=['GET'])
def hello():
    return 'Python OCR API Menyala!!!'

@app.route('/proceed-bca', methods=['POST'])
def proceed_bca() :
    return bca_controller(app)

@app.route('/proceed-bri', methods=['POST'])
def proceed_bri() :
    return bri_controller(app)
