from flask import Flask, jsonify, request
from flask_cors import CORS
from sympy import false

from services.check_is_zip import check_is_zip
from services.ocr_service import do_ocr
from services.ocr_service_zip import get_file_list_from_zip, proceed_ocr_zip
from services.utils import get_value_percentage, order_points, calculate_distance_between_2_points, clean_data

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Batas ukuran file hingga 16 MB

UPLOAD_FOLDER = 'uploads/'
EXTRACT_FOLDER = 'extracted_data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER

@app.route('/proceed', methods=['POST'])
def get_image():
    banyak_gambar = len(request.files)
    cleaned_data = None
    
    temp_arr = []
    list_sub_data = []
    is_zip = False

    for i in range(0, banyak_gambar):
        temp_arr.append(request.files.getlist('file[{}]'.format(i))[0])

    # cek apakah file adalah zip atau gambar
    if len(temp_arr) == 1:
        is_zip = check_is_zip(temp_arr)

    if is_zip:
        file_list = get_file_list_from_zip(temp_arr[0], app)

        if file_list == 400:
            return jsonify({
                'success': False,
                'data': 'Gagal mengekstrak Zip. Zip terproteksi password!'
            }), 400

        else:
            file_list.sort()
            list_data, list_sub_data = proceed_ocr_zip(file_list, app)
            cleaned_data = clean_data(list_data)

    else :
        # melakukan sorting terhadap file
        sorted_files = sorted(temp_arr, key=lambda x: x.filename)

        # disini ocr dijalankan
        list_data, list_sub_data = do_ocr(sorted_files, app)

        cleaned_data = clean_data(list_data)


    return jsonify({
        'data' : cleaned_data,
        'sub-data': list_sub_data
    })