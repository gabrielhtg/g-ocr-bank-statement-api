from flask import Flask
from flask_cors import CORS
from controller.bca_controller import ocr_bca
from controller.bri_controller import ocr_bri


app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Batas ukuran file hingga 16 MB

UPLOAD_FOLDER = 'uploads/'
EXTRACT_FOLDER = 'extracted_data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER

@app.route('/', methods=['GET'])
def hello():
    return 'Python OCR API Menyala!!!'

@app.route('/proceed-bca', methods=['POST'])
def proceed_bca() :
    return ocr_bca(app)

@app.route('/proceed-bri', methods=['POST'])
def proceed_bri() :
    return ocr_bri(app)
