from distutils.command.clean import clean

from flask import Flask, jsonify, request
from flask_cors import CORS
from services.check_is_zip import check_is_zip
from services.ocr_service import do_ocr
from services.utils import clean_data, get_file_list_from_zip

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Batas ukuran file hingga 16 MB

UPLOAD_FOLDER = 'uploads/'
EXTRACT_FOLDER = 'extracted_data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER

@app.route('/proceed', methods=['POST'])
def get_image():
    uploaded_files = request.files.getlist('files')
    bank_statement_type = request.form.get('bank-statement-type')

    if bank_statement_type == '' :
        return jsonify({
            'success': False,
            'data' : 'Tentukan jenis bank statement dulu!'
        }), 400

    is_zip = False

    # cek apakah file adalah zip atau gambar
    if len(uploaded_files) == 1:
        is_zip = check_is_zip(uploaded_files)

    if is_zip:
        file_list = get_file_list_from_zip(uploaded_files[0], app)

        if file_list == 400:
            return jsonify({
                'success': False,
                'data': 'Gagal mengekstrak Zip. Zip terproteksi password!'
            }), 400

        else:
            file_list.sort()
            list_data, list_sub_data = do_ocr(file_list, app, bank_statement_type, is_zip)

            if list_data == 400:
                return jsonify({
                    'success': False,
                    'data': 'Tipe dari bank statement tidak sama!'
                }), 400

            cleaned_data = clean_data(list_data)

    else :
        # melakukan sorting terhadap file
        sorted_files = sorted(uploaded_files, key=lambda x: x.filename)

        # disini ocr dijalankan
        list_data, list_sub_data = do_ocr(sorted_files, app, bank_statement_type, is_zip)

        if list_data == 400:
            return jsonify({
                'success': False,
                'data': 'Tipe dari bank statement tidak sama!'
            }), 400

        cleaned_data = clean_data(list_data)

    return jsonify({
        'transaction-data' : cleaned_data['data_transaction'], # cleaned data
        'analitics-data': {
            'saldo_awal' : list_sub_data[0],
            'mutasi_cr' : list_sub_data[1],
            'jumlah_mutasi_cr' : list_sub_data[2],
            'mutasi_db' : list_sub_data[3],
            'jumlah_mutasi_db' : list_sub_data[4],
            'saldo_akhir' : list_sub_data[5],
            'count_db_ocr' : cleaned_data['analitics_data']['count_db'],
            'count_cr_ocr' : cleaned_data['analitics_data']['count_cr'],
            'sum_cr' : cleaned_data['analitics_data']['sum_cr'],
            'sum_db' : cleaned_data['analitics_data']['sum_db'],
            'raw_sum_cr': cleaned_data['analitics_data']['raw_sum_cr'],
            'raw_sum_db': cleaned_data['analitics_data']['raw_sum_db'],
            'avg_db' : cleaned_data['analitics_data']['avg_db'],
            'avg_cr' : cleaned_data['analitics_data']['avg_cr'],
            'min_db' : cleaned_data['analitics_data']['min_db'],
            'min_cr' : cleaned_data['analitics_data']['min_cr'],
            'max_db' : cleaned_data['analitics_data']['max_db'],
            'max_cr' : cleaned_data['analitics_data']['max_cr'],
            'net_balance' : cleaned_data['analitics_data']['net_balance']
        } # list sub data
    })
