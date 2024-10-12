from flask import jsonify, request
from services.check_is_zip import checkIsZip
from services.bca_ocr_service import do_ocr_bca
from services.clean_bca_data import clean_bca_data
from services.get_file_list_from_zip import getFileListFromZip
from services.returnFailMessage import returnFailMessage

def bca_controller(app):
    uploaded_files = request.files.getlist('files')
    bank_statement_type = request.form.get('bank-statement-type')
    zip_password = ''
    
    if request.form.get('zip-password') :
        zip_password = request.form.get('zip-password')

    if bank_statement_type == '' :
        return returnFailMessage(False, 'Tentukan jenis bank statement dulu!')

    is_zip = False

    # cek apakah file adalah zip atau gambar
    if len(uploaded_files) == 1:
        is_zip = checkIsZip(uploaded_files)

    if is_zip:
        # melakukan ekstraksi dari zip dan menyimpannya ke dalam list
        file_list = getFileListFromZip(uploaded_files[0], app, zip_password)
        
        # return jika zip gagal diekstrak karena terproteksi password
        if file_list == 400:
            return returnFailMessage(False, 'Gagal mengekstrak zip! Password salah!')

        else:
            # melakukan sorting berdasarkan nama file
            file_list.sort()
            
            # melakukan process ocr
            list_data, list_sub_data = do_ocr_bca(file_list, app, bank_statement_type, is_zip)

            # return jika tipe data bank statement tidak sama dengan yang diinput sebelumnya
            if list_data == 400:
                return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

            cleaned_data = clean_bca_data(list_data)
            
            if cleaned_data == 400:
                return returnFailMessage(False, 'Pastikan seluruh halaman dari bank statement sudah lengkap diupload!')

    else :
        # melakukan sorting terhadap file
        sorted_files = sorted(uploaded_files, key=lambda x: x.filename)

        # disini ocr dijalankan
        list_data, list_sub_data = do_ocr_bca(sorted_files, app, bank_statement_type, is_zip)
        

        if list_data == 400:
            return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

        cleaned_data = clean_bca_data(list_data)
        
        if cleaned_data == 400:
            return returnFailMessage(False, 'Pastikan seluruh halaman dari bank statement sudah lengkap diupload!')

    try :
        return jsonify({
            'transaction-data'      : cleaned_data['data_transaction'], # cleaned data
            'analitics-data'        : {
                'saldo_awal'            : list_sub_data[0],
                'mutasi_cr'             : list_sub_data[1],
                'jumlah_mutasi_cr'      : list_sub_data[2],
                'mutasi_db'             : list_sub_data[3],
                'jumlah_mutasi_db'      : list_sub_data[4],
                'saldo_akhir'           : list_sub_data[5],
                'count_db_ocr'          : cleaned_data['analitics_data']['count_db'],
                'count_cr_ocr'          : cleaned_data['analitics_data']['count_cr'],
                'sum_cr'                : cleaned_data['analitics_data']['sum_cr'],
                'sum_db'                : cleaned_data['analitics_data']['sum_db'],
                'raw_sum_cr'            : cleaned_data['analitics_data']['raw_sum_cr'],
                'raw_sum_db'            : cleaned_data['analitics_data']['raw_sum_db'],
                'avg_db'                : cleaned_data['analitics_data']['avg_db'],
                'avg_cr'                : cleaned_data['analitics_data']['avg_cr'],
                'min_db'                : cleaned_data['analitics_data']['min_db'],
                'min_cr'                : cleaned_data['analitics_data']['min_cr'],
                'max_db'                : cleaned_data['analitics_data']['max_db'],
                'max_cr'                : cleaned_data['analitics_data']['max_cr'],
                'net_balance'           : cleaned_data['analitics_data']['net_balance']
            }
        })
        
    except IndexError as e :
        return returnFailMessage(False, "Pastikan halaman bank statement sudah lengkap!")