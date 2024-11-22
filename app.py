import os
from flask import Flask
from flask_cors import CORS

from waitress import serve

from controller.bca_controller import bcaController
from controller.bni_controller import bniController
from controller.bri_controller import briController
from controller.cimb_controller import cimbController
from controller.danamon_controller import danamonController
from controller.mandiri_controller import mandiriController
from controller.ocbc_controller import ocbcController
from controller.permata_controller import permataController

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Batas ukuran file hingga 16 MB

UPLOAD_FOLDER = 'uploads/'
EXTRACT_FOLDER = 'extracted_data/'
PDF_EXTRACT_FOLDER = 'extracted_pdf/'
BELL = 'bell.wav'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER
app.config['PDF_EXTRACT_FOLDER'] = PDF_EXTRACT_FOLDER
app.config['BELL'] = BELL

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(EXTRACT_FOLDER):
    os.makedirs(EXTRACT_FOLDER, exist_ok=True)
if not os.path.exists(PDF_EXTRACT_FOLDER):
    os.makedirs(PDF_EXTRACT_FOLDER, exist_ok=True)
    
if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    #We now use this syntax to server our app. 
    serve(app, host='0.0.0.0', port=5000)

@app.route('/', methods=['GET'])
def hello():
    return 'Python OCR API Menyala!!!'

@app.route('/proceed-bca', methods=['POST'])
def proceed_bca() :
    return bcaController(app)

@app.route('/proceed-bri', methods=['POST'])
def proceed_bri() :
    return briController(app)

@app.route('/proceed-permata', methods=['POST'])
def proceedPermata () : 
    return permataController(app)

@app.route('/proceed-danamon', methods=['POST'])
def proceedDanamon () : 
    return danamonController(app)

@app.route('/proceed-bni', methods=['POST'])
def proceedBni () : 
    return bniController(app)

@app.route('/proceed-cimb', methods=['POST'])
def proceedCimb () : 
    return cimbController(app)

@app.route('/proceed-ocbc', methods=['POST'])
def proceedOcbc () : 
    return ocbcController(app)

@app.route('/proceed-mandiri', methods=['POST'])
def proceedMandiri () : 
    return mandiriController(app)
