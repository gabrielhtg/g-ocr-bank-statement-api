import os
import statistics
import zipfile
from io import BytesIO

from flask import jsonify
import numpy as np
from werkzeug.utils import secure_filename

import pyzipper

def clean_data (array) :
    arr_temp = []
    count_db = 0
    count_cr = 0
    sum_db = 0.0
    sum_cr = 0.0
    list_cr = []
    list_db = []
    
    for e in array:
        col_zero = ''
        col_one = ''
        col_two = ''
        col_three = ''
        col_four = ''
        current_filename = None
        current_page = None
        
        for e_ in e:
            if e_['col'] == 0:
                col_zero = col_zero + ' ' +  e_['text']

            if e_['col'] == 1:
                col_one = col_one + ' ' + e_['text']

            if e_['col'] == 2:
                col_two = col_two + ' ' + e_['text']

            if e_['col'] == 3:
                col_three = col_three + ' ' + e_['text']

            if e_['col'] == 4:
                col_four = col_four + ' ' + e_['text']

            current_filename = e_['filename']
            current_page = e_['page']

        # print('Col three :', col_three)
        # print('Halaman   :', current_filename)
        # print()

        if col_three != '' :
            col_three = (col_three
                        .strip()
                        .replace(' ', '')
                        .replace(',', '')
                        .replace('o', '0')
                        .replace('O', '0')
                        .replace('u', 'D')
                        .replace('.', ''))

            if 'D' in col_three or 'B' in col_three:
                if col_three[-1] == '2':
                    col_three = col_three[:-1] + 'B'

                col_three = col_three[:-2]
                col_three = col_three[:-2] + '.' + col_three[-2:]

                try :
                    sum_db += float(col_three)
                except ValueError:
                    return 400
                    
                list_db.append(float(col_three))

                try:
                    col_three = "{:,.2f}".format(float(col_three)) + ' DB'
                except ValueError:
                    col_three = col_three + ' !!'

            else:
                col_three = col_three[:-2] + '.' + col_three[-2:]
                sum_cr += float(col_three)
                list_cr.append(float(col_three))

                try:
                    col_three = "{:,.2f}".format(float(col_three))
                except ValueError:
                    col_three = col_three + ' !!'

        if col_four != '' :
            col_four = (col_four.replace(' ', '')
                         .replace(',', '')
                         .replace('o', '0')
                         .replace('O', '0')
                         .replace('.', ''))

            col_four = col_four[:-2] + '.' + col_four[-2:]
            col_four = "{:,.2f}".format(float(col_four))

        if 'DB' in col_three:
            count_db += 1

        if ' CR ' in col_one or 'CR ' in col_one or ' CR' in col_one or 'KR ' in col_one or 'KR ' in col_one or ' KR' in col_one :
            count_cr += 1

        arr_temp.append(
            [
                col_zero.strip(),
                col_one.strip(),
                col_two.strip(),
                col_three,
                col_four,
                current_filename.strip(),
                current_page
            ]
        )

    return {
        'data_transaction' : arr_temp,
        'analitics_data' : {
            'count_db' : count_db,
            'count_cr' : count_cr,
            'sum_cr' : "{:,.2f}".format(sum_cr),
            'raw_sum_cr' : sum_cr,
            'raw_sum_db' : sum_db,
            'sum_db' : "{:,.2f}".format(sum_db),
            'avg_cr' : "{:,.2f}".format(statistics.mean(list_cr)),
            'avg_db' : "{:,.2f}".format(statistics.mean(list_db)),
            'min_db' : "{:,.2f}".format(min(list_db)),
            'min_cr' : "{:,.2f}".format(min(list_cr)),
            'max_db' : "{:,.2f}".format(max(list_db)),
            'max_cr' : "{:,.2f}".format(max(list_cr)),
            'net_balance' : "{:,.2f}".format(sum_cr - sum_db)
        }
    }

def contains_number(s):
    return any(char.isdigit() for char in s)

# ! DEPRECATED
# Fungsi ini digunakan untuk melakukan ekstraksi terhadap zip
# def get_file_list_from_zip(data_file, app, zip_password):
#     # Ekstrak file zip ke folder EXTRACT_FOLDER
#     with zipfile.ZipFile(BytesIO(data_file.read()), 'r') as zip_ref:
#         try:
#             file_list = zip_ref.namelist()
#             zip_ref.extractall(app.config['EXTRACT_FOLDER'])
#         except RuntimeError:
#             return 400

#     return file_list

# fungsi ini digunakan untuk melakukan ekstraksi terhadap zip
def get_file_list_from_zip(data_file, app, zip_password):
    # Ekstrak file zip ke folder EXTRACT_FOLDER
    with pyzipper.AESZipFile(BytesIO(data_file.read()), 'r') as zip_ref:
        try:
            # Gunakan kata sandi untuk membuka zip
            zip_ref.pwd = zip_password.encode('utf-8')
            
            file_list = zip_ref.namelist()
            zip_ref.extractall(app.config['EXTRACT_FOLDER'])
        except (RuntimeError, pyzipper.BadZipFile, pyzipper.LargeZipFile) as e:
            return 400

    return file_list

def get_file_list_from_protected_zip(data_file, app, password):
    file = data_file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Ekstrak file zip ke folder EXTRACT_FOLDER
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # 'setpassword' method is used to give a password to the 'Zip'
        zip_ref.setpassword(pwd=bytes(password, 'utf-8'))
        file_list = zip_ref.namelist()
        zip_ref.extractall(app.config['EXTRACT_FOLDER'])

    # os.remove(file_path)

    return file_list

def is_current_page_the_right_bank_statement_type (bank_statement_type, ocr_text) :
    if int(bank_statement_type) == 1 :
        if 'rekening giro' in ocr_text.lower() :
            return True

        return False

    if int(bank_statement_type) == 2 :
        if 'rekening tahapan' in ocr_text.lower() :
            return True

        return False
    
def return_fail_message(taskStatus, message) :
    return jsonify({
        'success' : taskStatus,
        'data' : message
    }), 400
    