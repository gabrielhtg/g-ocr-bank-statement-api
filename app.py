from asyncio import threads
import logging
from logging.handlers import TimedRotatingFileHandler
import multiprocessing
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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER
app.config['PDF_EXTRACT_FOLDER'] = PDF_EXTRACT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(EXTRACT_FOLDER):
    os.makedirs(EXTRACT_FOLDER, exist_ok=True)
if not os.path.exists(PDF_EXTRACT_FOLDER):
    os.makedirs(PDF_EXTRACT_FOLDER, exist_ok=True)
    
# Set up logger with TimedRotatingFileHandler
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, 'app.log')

# Logger setup with rotating log files
log_handler = TimedRotatingFileHandler(
    log_file, when='midnight', interval=1, backupCount=7
)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler.setLevel(logging.INFO)

# Adding both rotating file handler and stream handler (for console output)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(logging.StreamHandler())
    
@app.route('/', methods=['GET'])
def hello():
    return 'Python OCR API Menyala!!!'

@app.route('/proceed-bca', methods=['POST'])
def proceed_bca() :
    return bcaController(app, logger)

@app.route('/proceed-bri', methods=['POST'])
def proceed_bri() :
    return briController(app, logger)

@app.route('/proceed-permata', methods=['POST'])
def proceedPermata () : 
    return permataController(app, logger)

@app.route('/proceed-danamon', methods=['POST'])
def proceedDanamon () : 
    return danamonController(app, logger)

@app.route('/proceed-bni', methods=['POST'])
def proceedBni () : 
    return bniController(app, logger)

@app.route('/proceed-cimb', methods=['POST'])
def proceedCimb () : 
    return cimbController(app, logger)

@app.route('/proceed-ocbc', methods=['POST'])
def proceedOcbc () : 
    return ocbcController(app, logger)

@app.route('/proceed-mandiri', methods=['POST'])
def proceedMandiri () : 
    return mandiriController(app, logger)

if __name__ == "__main__":
    num_threads = multiprocessing.cpu_count()
    print('-' * 100)
    print(f'Banyak threads : {num_threads}')
    print('Api Flask Is Running!!!')
    print('-' * 100)
    serve(app, host='0.0.0.0', port=5000, threads=num_threads)
    